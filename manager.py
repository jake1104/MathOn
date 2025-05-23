from sympy import *
from math import *

# 파일 시작 부분에 추가
debug_mode = False

Symbols = []
class Eq:
    def __init__(self, name, variables, eq):
        self.name = name
        self.variable = variables
        self.eq = eq
Eqs = []

def set_debug(mode):
    global debug_mode
    if isinstance(mode, bool):
        debug_mode = mode
        print(f"디버그 모드가 {'켜졌습니다' if mode else '꺼졌습니다'}")
    else:
        print("debug() 함수는 True 또는 False 값만 받을 수 있습니다")

def expansion(expression):
    if expression.count("=") == 1:
        left_side = expression.split("=")[0]
        right_side = expression.split("=")[1]
        return expand(simplify(f"{left_side}-({right_side})"))
    else:
        return expand(simplify(expression))

def factorization(expression):
    if expression.count("=") == 1:
        left_side = expression.split("=")[0]
        right_side = expression.split("=")[1]
        return factor(simplify(f"{left_side}-({right_side})"))
    else:
        return factor(simplify(expression))

def pretty_print(expression):
    # 기본 변환
    result = str(expression).replace("**", "^").replace("*", "")
    
    # 기존 공백 제거 후 +, -, = 앞뒤로 공백 한 칸씩 추가
    result = result.replace(" ", "")  # 기존 공백 모두 제거
    result = result.replace("+", " + ").replace("-", " - ").replace("=", " = ")
    
    # 맨 앞에 있는 공백 제거 (음수 시작인 경우를 위해)
    result = result.strip()
    if result.startswith("- "):
        result = "-" + result[2:]
        
    return result

def pretty_to_math(expression):
    # 공백 제거
    result = str(expression).strip()
    # ^ 를 ** 로 변환
    result = result.replace("^", "**")
    
    # 숫자와 문자 사이 곱셈 기호 추가
    new_result = ''
    for i in range(len(result)-1):
        if (result[i].isdigit() and result[i+1].isalpha()) or (result[i].isalpha() and result[i+1].isdigit()):
            new_result += result[i] + '*'
        else:
            new_result += result[i]
    new_result += result[-1]
    result = new_result

    # 괄호 처리
    result = result.replace(")(", ")*(")
    for c in "abcdefghijklmnopqrstuvwxyzαβγδεζηθικλμνξοπρστυφχψω":
        result = result.replace(f"){c}", f")*{c}")
        result = result.replace(f"{c}(", f"{c}*(")
    
    return result



def find_intersection(ranges1, ranges2, strict1=False, strict2=False):
    if debug_mode:
        print(f"Debug: Finding intersection between {ranges1} and {ranges2}")
    
    result = []
    for r1 in ranges1:
        for r2 in ranges2:
            # 단일점인 경우 (방정식의 해)
            if abs(r1[0] - r1[1]) < 1e-10:  # r1이 단일점
                point = r1[0]
                # r2가 범위이고 그 범위 안에 point가 있는지 확인
                if r2[0] < point < r2[1] or (not strict2 and (abs(r2[0] - point) < 1e-10 or abs(r2[1] - point) < 1e-10)):
                    result.append((point, point))
            elif abs(r2[0] - r2[1]) < 1e-10:  # r2가 단일점
                point = r2[0]
                # r1이 범위이고 그 범위 안에 point가 있는지 확인
                if r1[0] < point < r1[1] or (not strict1 and (abs(r1[0] - point) < 1e-10 or abs(r1[1] - point) < 1e-10)):
                    result.append((point, point))
            else:  # 둘 다 범위인 경우
                start = max(r1[0], r2[0])
                end = min(r1[1], r2[1])
                if start < end or (not (strict1 or strict2) and abs(start - end) < 1e-10):
                    result.append((start, end))
    
    if debug_mode:
        print(f"Debug: Intersection result: {result}")
    
    return result if result else None

def format_range_output(ranges, var_name='x'):
    if not ranges:
        return "해가 없습니다"
    
    parts = []
    for start, end in ranges:
        if abs(start - end) < 1e-10:  # 단일점
            parts.append(f"{var_name} = {pretty_print(start)}")
        else:
            if start == float('-inf'):
                parts.append(f"{var_name} < {pretty_print(end)}")
            elif end == float('inf'):
                parts.append(f"{var_name} > {pretty_print(start)}")
            else:
                parts.append(f"{pretty_print(start)} < {var_name} < {pretty_print(end)}")
    
    return " or ".join(parts)

def solve_equation(expression):
    if debug_mode:
        print(f"Debug: Input expression: {expression}")
    
    # 수식을 sympy가 이해할 수 있는 형태로 변환
    expression = pretty_to_math(expression.strip())
    
    # 변수 확인
    allowed_vars = ['x', 'y', 'z']
    used_vars = []
    for var in allowed_vars:
        if var in expression:
            used_vars.append(var)
    
    if len(used_vars) == 0:
        if any(c.isalpha() for c in expression):  # 다른 문자가 변수로 사용된 경우
            return "x, y, z 변수만 사용할 수 있습니다."
        # 변수가 없는 경우 (항등식)
        if simplify(expression) == 0:
            return "모든 실수"
        else:
            return "해가 없습니다"
    
    # 연립방정식 처리
    if len(used_vars) > 1:
        try:
            if debug_mode:
                print(f"Debug: Solving system with vars {used_vars}")
                print(f"Debug: Expression {expression}")
            
            # 등호 처리
            if "=" in expression:
                left, right = expression.split("=")
                equation = f"({left})-({right})"
            else:
                equation = expression
                
            if debug_mode:
                print(f"Debug: Parsed equation: {equation}")
            
            equation = parse_expr(equation)
            # 기존 해 가져오기
            existing_solutions = {}
            for var in used_vars:
                symbol = next((s for s in Symbols if s[0] == var), None)
                if symbol:
                    existing_solutions[var] = symbol[1]
                    if debug_mode:
                        print(f"Debug: Existing solutions for {var}: {symbol[1]}")
                else:
                    return f"변수 {var}의 해가 정의되지 않았습니다"
            
            # 모든 가능한 조합 확인
            valid_solutions = []
            for x_range in existing_solutions[used_vars[0]]:
                x_val = x_range[0]  # 시작점
                if abs(x_range[0] - x_range[1]) > 1e-10:  # 범위인 경우
                    x_val = x_range[0]  # 범위의 시작점 사용
                
                for y_range in existing_solutions[used_vars[1]]:
                    y_val = y_range[0]  # 시작점
                    if abs(y_range[0] - y_range[1]) > 1e-10:  # 범위인 경우
                        y_val = y_range[0]  # 범위의 시작점 사용
                    
                    if debug_mode:
                        print(f"Debug: Testing {used_vars[0]}={x_val}, {used_vars[1]}={y_val}")
                    
                    result = equation.subs([(Symbol(used_vars[0]), x_val), 
                                          (Symbol(used_vars[1]), y_val)])
                    
                    if debug_mode:
                        print(f"Debug: Result = {result}")
                    
                    if abs(float(result)) < 1e-10:
                        valid_solutions.append((x_val, y_val))
                        if debug_mode:
                            print(f"Debug: Found valid solution!")
            
            if not valid_solutions:
                return "해가 없습니다"
            
            # 해 업데이트
            for i, var in enumerate(used_vars):
                new_ranges = [(sol[i], sol[i]) for sol in valid_solutions]
                Symbols[:] = [s for s in Symbols if s[0] != var]
                Symbols.append((var, new_ranges, False))
            
            # 결과 출력 - 중괄호로 묶어서 출력
            solutions_str = []
            for solution in valid_solutions:
                parts = []
                for i, var in enumerate(used_vars):
                    parts.append(f"{var} = {pretty_print(solution[i])}")
                solutions_str.append("{" + ", ".join(parts) + "}")
            
            return " or ".join(solutions_str)
        except Exception as e:
            if debug_mode:
                print(f"Debug: Exception in solving system: {e}")
            return "해를 구할 수 없습니다"
    
    # 단일 변수 방정식 처리 (기존 코드)
    var_name = used_vars[0]
    # 등호나 부등호로 분리
    is_equal = False
    is_strict = True
    if "=" in expression:
        if ">=" in expression:
            left, right = expression.split(">=")
            equation = f"{left}-({right})"
            is_greater = True
            is_equal = True
            is_strict = False
        elif "<=" in expression:
            left, right = expression.split("<=")
            equation = f"({right})-({left})"
            is_greater = False
            is_equal = True
            is_strict = False
        else:
            left, right = expression.split("=")
            equation = f"{left}-({right})"
            is_equal = True
            is_strict = False
    elif ">" in expression:
        left, right = expression.split(">")
        equation = f"{left}-({right})"
        is_greater = True
        is_strict = True
    elif "<" in expression:
        left, right = expression.split("<")
        equation = f"({right})-({left})"
        is_greater = False
        is_strict = True
    elif ">=" in expression:
        left, right = expression.split(">=")
        equation = f"{left}-({right})"
        is_greater = True
        is_strict = False
    elif "<=" in expression:
        left, right = expression.split("<=")
        equation = f"({right})-({left})"
        is_greater = False
        is_strict = False
    else:
        return None
    
    # 변 찾기
    vars = list(simplify(equation).free_symbols)
    if len(vars) > 1:
        return "방정식에는 하나의 변수만 사용할 수 있습니다."
    elif len(vars) == 0:  # 변수가 없는 경우 (항등식)
        # 식이 항 참인지 확인
        if simplify(equation) == 0:
            return "모든 실수"
        else:
            return "해가 없습니다"
    
    var_name = str(vars[0])
    solutions = solve(equation, vars[0])
    
    # 새로운 해 범위 계산
    new_ranges = None
    if not is_equal:  # 부등식인 경우
        if equation.replace(" ", "") == "x":  # x>0 또는 x<0 같은 단순한 경우
            if is_greater:
                new_ranges = [(0, float('inf'))]
            else:
                new_ranges = [(float('-inf'), 0)]
        elif isinstance(solutions, list) and len(solutions) > 1:
            solutions = sorted([float(sol) for sol in solutions])
            if is_greater:
                new_ranges = [(solutions[1], float('inf'))]
            else:
                new_ranges = [(solutions[0], solutions[1])]
        elif len(solutions) == 1:
            sol_value = float(solutions[0])
            if is_greater:
                new_ranges = [(sol_value, float('inf'))]
            else:
                new_ranges = [(float('-inf'), sol_value)]
    else:  # 방정식인 경우
        if solutions:
            solutions = sorted([float(sol) for sol in solutions])
            new_ranges = [(sol, sol) for sol in solutions]
    
    # 기존 해와 교집합 계산
    existing_symbol = next((s for s in Symbols if s[0] == var_name), None)
    if existing_symbol:
        intersection = find_intersection(existing_symbol[1], new_ranges, 
                                      existing_symbol[2], is_strict)
        if not intersection:
            return "해가 없습니다"
        Symbols[:] = [s for s in Symbols if s[0] != var_name]
        Symbols.append((var_name, intersection, False))  # 방정식은 항상 is_strict=False
    else:
        Symbols.append((var_name, new_ranges, is_strict))
    
    # 결과 출력
    ranges = next(s[1] for s in Symbols if s[0] == var_name)
    return format_range_output(ranges, var_name)

# 상수, 변수, 함수 구분 위한 리스트 추가
CONSTANTS = list('abcdpq')
VARIABLES = list('xyz')
FUNCTIONS = list('fgh')
SOLUTIONS = ['α', 'β', 'γ', 'δ']  # 그리스 문자

def is_equation_or_function(input_str):
    # 함수 정의나 방정인지 확인
    if '(' in input_str:
        if any(op in input_str for op in ["=", ">", "<", ">=", "<="]):
            return 'equation'  # 등호나 부등호가 있으면 방정식
        name = input_str.split('(')[0].strip()
        if len(name) == 1:
            if name in FUNCTIONS:
                return 'function'
    return 'equation'  # 기본적으로 방정식으로 처리

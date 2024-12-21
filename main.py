from sympy import *
from math import *
from graph import *
from manager import *

print(
    "MathOn v1.0.1 2023y/7m/8d (Made By Jake, Use Python)\nType \"help()\", for more information and type \"exit()\", for close console."
)

while True:
    shell_input = input("MO >>> ")
    if shell_input == "exit()":
        print("Close Console")
        break
    elif shell_input == "help()":
        print(
            "This is a all command of MathOn programming language\n\n"
            "help() - print all command\n"
            "features() - print all features of Mathon 2.0.1\n"
            "exit() - close console\n"
            "greek() - print all greek alphabet\n"
            "symbol name - print value of symbol name\n"
            "eq name - print value of eq name\n"
            "debug(True/False) - 디버그 모드 켜기/끄기\n"
            "방정식/부등식을 입력하면 해를 구함\n"
            "함수를 입력하면 함수값을 구함\n"
            "if you input nothing then it print nothing"
        )
    elif shell_input == "features()":
        print(
            "Mathon 2.0.1 features\n"
            "- add features\n"
            "- add function\n"
            "- add func graph"
        )

    elif shell_input == "greek()":
        print("small letter:   α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ τ υ φ χ ψ ω")
        print("capital letter: Α Β Γ Δ Ε Ζ Η Θ Ι Κ Λ Μ Ν Ξ Ο Π Ρ Σ Τ Υ Φ Χ Ψ Ω")
    elif (
        "(" in shell_input and
        ")" in shell_input and
        len(shell_input.split("(")[0]) == 1
    ):
        name = shell_input.split("(")[0]
        if shell_input.count("=") == 1:
            # 함수 정의하는 경우
            is_in = False
            for eq in Eqs:
                if name == eq.name:
                    print(f"Traceback (most recent call last):\n  File \"<stdin>\", line 1, in <module>\nNameError: name '{name}' already exists.")
                    is_in = True
                    break
            if not is_in:
                variables = shell_input.split("(")[1].split(")")[0].replace(" ", "").split(",")
                expression = pretty_to_math(shell_input.split("=")[1])
                # sympy Symbol 객체 생성
                for var in variables:
                    Symbol(var)
                # 식 검증
                used_vars = list(simplify(expression).free_symbols)
                # 정의되지 않은 변수 확인
                undefined_vars = []
                for var in used_vars:
                    var_str = str(var)
                    if var_str not in variables and var_str not in [s[0] for s in Symbols]:
                        undefined_vars.append(var_str)
                
                if undefined_vars:
                    print(f"Traceback (most recent call last):\n  File \"<stdin>\", line 1, in <module>\nNameError: undefined variables: {', '.join(undefined_vars)}")
                else:
                    Eqs.append(Eq(name, variables, expression))
                    print(f"Successfully defined function '{name}'")
        else:
            # 함수 호출하는 경우 
            found = False
            for eq in Eqs:
                if name == eq.name:
                    found = True
                    input_vars = shell_input.split("(")[1].split(")")[0].replace(" ", "").split(",")
                    if len(input_vars) != len(eq.variable):
                        print(f"Traceback (most recent call last):\n  File \"<stdin>\", line 1, in <module>\nValueError: {eq.name}() takes {len(eq.variable)} arguments but {len(input_vars)} were given")
                    else:
                        # 함수 이름과 변수를 포함한 전체 정의를 출력
                        if input_vars == eq.variable:  # 원래 변수와 동일한 경우
                            print(pretty_print(f"{name}({','.join(eq.variable)})={eq.eq}"))
                            print(draw_function(func=lambdify(input_vars, eq.eq, 'numpy')))
                        else:  # 다른 값이 입력된 경우
                            result = eq.eq
                            for i in range(len(input_vars)):
                                result = expansion(result.replace(eq.variable[i], f"({input_vars[i]})"))
                            # 함수 호출 부분은 공백 없이, 결과 부분만 공백 포함
                            print(f"{name}({','.join(input_vars)}) = {pretty_print(result)}")
                    break
            if not found:
                print(f"Traceback (most recent call last):\n  File \"<stdin>\", line 1, in <module>\nNameError: name '{name}' is not defined.")
    elif any(op in shell_input for op in ["=", ">", "<", ">=", "<="]):
        input_type = is_equation_or_function(shell_input)
        
        if input_type == 'function':
            # 함수 정의/호출 처리
            name = shell_input.split("(")[0]
            if shell_input.count("=") == 1:
                # 수 정의하는 경우
                is_in = False
                for eq in Eqs:
                    if name == eq.name:
                        print(f"Traceback (most recent call last):\n  File \"<stdin>\", line 1, in <module>\nNameError: name '{name}' already exists.")
                        is_in = True
                        break
                if not is_in:
                    variables = shell_input.split("(")[1].split(")")[0].replace(" ", "").split(",")
                    expression = pretty_to_math(shell_input.split("=")[1])
                    # sympy Symbol 객체 생성
                    for var in variables:
                        Symbol(var)
                    # 식 검증
                    used_vars = list(simplify(expression).free_symbols)
                    # 정의되지 않은 변수 확인
                    undefined_vars = []
                    for var in used_vars:
                        var_str = str(var)
                        if var_str not in variables and var_str not in [s[0] for s in Symbols]:
                            undefined_vars.append(var_str)
                
                    if undefined_vars:
                        print(f"Traceback (most recent call last):\n  File \"<stdin>\", line 1, in <module>\nNameError: undefined variables: {', '.join(undefined_vars)}")
                    else:
                        Eqs.append(Eq(name, variables, expression))
                        print(f"Successfully defined function '{name}'")
            else:
                # 수 호출하는 경우 
                found = False
                for eq in Eqs:
                    if name == eq.name:
                        found = True
                        input_vars = shell_input.split("(")[1].split(")")[0].replace(" ", "").split(",")
                        if len(input_vars) != len(eq.variable):
                            print(f"Traceback (most recent call last):\n  File \"<stdin>\", line 1, in <module>\nValueError: {eq.name}() takes {len(eq.variable)} arguments but {len(input_vars)} were given")
                        else:
                            # 함수 이름과 변수를 포함한 전체 정의를 출력
                            if input_vars == eq.variable:  # 원래 변수와 동일한 경우
                                print(pretty_print(f"{name}({','.join(eq.variable)})={eq.eq}"))
                            else:  # 다른 이 입력된 경우
                                result = eq.eq
                                for i in range(len(input_vars)):
                                    result = expansion(result.replace(eq.variable[i], f"({input_vars[i]})"))
                                # 함수 호출 부분은 공백 없이, 결과 부분만 공백 포함
                                print(f"{name}({','.join(input_vars)}) = {pretty_print(result)}")
                        break
                if not found:
                    print(f"Traceback (most recent call last):\n  File \"<stdin>\", line 1, in <module>\nNameError: name '{name}' is not defined.")
        elif input_type == 'equation' or not '(' in shell_input:
            # 방정식 처리
            result = solve_equation(shell_input)
            if result:
                print(result)
        else:
            print(f"Traceback (most recent call last):\n  File \"<stdin>\", line 1, in <module>\nNameError: Invalid expression")
    elif shell_input in ["Jake", "jake", "JAKE"]:
        print("Jake made this programming language")
    elif shell_input.startswith("debug(") and shell_input.endswith(")"):
        value = shell_input[6:-1].strip().lower()
        if value not in ["true", "false"]:
            print(
                f"Traceback (most recent call last):\n  File \"<stdin>\", line 1, in <module>\nNameError: name '{shell_input}' is not defined."
            )
        else:
            set_debug(value == "true")
    elif shell_input in [s[0] for s in Symbols]:
        if debug_mode:
            print(f"Debug: Looking for variable '{shell_input}' in {Symbols}")
        symbol = next(s for s in Symbols if s[0] == shell_input)
        if symbol[1]:  # 해가 는 경우
            print(format_range_output(symbol[1]))
        else:
            print("해가 없습니다")
    else:
        try:
            # 다항식 처리
            expr = pretty_to_math(shell_input)
            expanded = expansion(expr)
            factored = factorization(expr)
            
            if str(expanded) != str(factored):
                print(f"전개식: {pretty_print(expanded)}")
                print(f"인수분해: {pretty_print(factored)}")
            else:
                print(pretty_print(expanded))
        except Exception as e:
            if debug_mode:
                print(f"Debug: Exception: {e}")
            if shell_input.replace(" ", "") == "":
                pass
            else:
                print(
                    f"Traceback (most recent call last):\n  File \"<stdin>\", line 1, in <module>\nNameError: name '{shell_input}' is not defined."
                )
    shell_input = ""

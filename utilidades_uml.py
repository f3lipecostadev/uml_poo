# utilidades_uml.py
from IPython.display import Image, display
from pathlib import Path
import subprocess
import ast

def gerar_diagrama(nome_arquivo, codigo_uml):
    arquivo_puml = Path(f"{nome_arquivo}.puml")
    arquivo_png = Path(f"{nome_arquivo}.png")
    arquivo_puml.write_text(codigo_uml, encoding="utf-8")
    subprocess.run(["java", "-jar", "plantuml.jar", str(arquivo_puml)], check=True)
    display(Image(filename=str(arquivo_png)))

def python_para_plantuml(codigo_python):
    arvore = ast.parse(codigo_python)
    classes = []
    herancas = []
    for no in arvore.body:
        if isinstance(no, ast.ClassDef):
            nome_classe = no.name
            atributos = set()
            metodos = []
            # Herança
            for base in no.bases:
                if isinstance(base, ast.Name):
                    herancas.append((base.id, nome_classe))
            # Métodos e atributos
            for item in no.body:
                if isinstance(item, ast.FunctionDef):
                    metodos.append(item.name)
                    for sub_no in ast.walk(item):
                        if (
                            isinstance(sub_no, ast.Attribute)
                            and isinstance(sub_no.value, ast.Name)
                            and sub_no.value.id == "self"
                        ):
                            atributos.add(sub_no.attr)
            classes.append({
                "nome": nome_classe,
                "atributos": sorted(atributos),
                "metodos": metodos
            })
    uml = ["@startuml", ""]
    for classe in classes:
        uml.append(f"class {classe['nome']} {{")
        for atributo in classe["atributos"]:
            uml.append(f"    - {atributo}")
        if classe["atributos"]:
            uml.append("")
        for metodo in classe["metodos"]:
            uml.append(f"    + {metodo}()")
        uml.append("}")
        uml.append("")
    for pai, filho in herancas:
        uml.append(f"{pai} <|-- {filho}")
    uml.append("")
    uml.append("@enduml")
    return "\n".join(uml)

def gerar_diagrama_python(nome_arquivo, codigo_python):
    codigo_uml = python_para_plantuml(codigo_python)
    print("=== PlantUML Gerado ===")
    print(codigo_uml)
    gerar_diagrama(nome_arquivo, codigo_uml)


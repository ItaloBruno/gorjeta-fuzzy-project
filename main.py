"""
Este algoritmo consiste em calcular o valor da gorjeta em um restaurante
levando em consideração as avaliações da comida e do atendimento prestado ao cliente.

Entradas:
    Qualidade da comida:
    - universo (intervalo de valores nítidos): 0 - 10
    - conjunto nebuloso: horrível, dá pra ir, magnífica

    Qualidade do serviço:
    - universo (intervalo de valores nítidos): 0 - 10
    - conjunto nebuloso: ruim, mais ou menos, só o mi

Saída:
    Gorjeta do atendente
    - universo (intervalo de valores nítidos): 0 - 25%
    - conjunto nebuloso: baixa, média, alta

Regras de decisão:
    - SE o serviço for só o mi OU a comida for magnífica ENTÃO a gorjeta deve ser alta :D
    - SE o serviço for mais ou menos, ENTÃO a gorjeta deve ser média :|
    - SE o serviço for ruim E a comida for horrível ENTÃO a gorjeta deve ser baixa :(
"""

import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl

# Definindo as variáveis do nosso problema (entrada e saída)
qualidade_comida = ctrl.Antecedent(np.arange(0, 11, 1), "comida")
qualidade_servico = ctrl.Antecedent(np.arange(0, 11, 1), "servico")
porcentagem_gorjeta = ctrl.Consequent(np.arange(0, 26, 1), "gorjeta")

# Cria automaticamente o mapeamento entre valores nítidos e difusos
# usando uma função de pertinência padrão (triângulo)
qualidade_comida.automf(names=["horrível", "dá pra ir", "magnífica"])
qualidade_servico.automf(names=["ruim", "mais ou menos", "só o mi"])
porcentagem_gorjeta.automf(names=["baixa", "média", "alta"])

porcentagem_gorjeta["baixa"] = fuzzy.trimf(porcentagem_gorjeta.universe, [0, 0, 13])
porcentagem_gorjeta["média"] = fuzzy.trimf(porcentagem_gorjeta.universe, [0, 13, 25])
porcentagem_gorjeta["alta"] = fuzzy.trimf(porcentagem_gorjeta.universe, [13, 25, 25])

# Mostrando os gráficos para cada uma das entradas e saídas
# qualidade_comida.view()
# qualidade_servico.view()
# porcentagem_gorjeta.view()

# Definindo as regras para fazer o cálculo da final porcentagem da gorjeta
regra_1 = ctrl.Rule(
    qualidade_servico["só o mi"] | qualidade_comida["magnífica"],
    porcentagem_gorjeta["alta"],
)
regra_2 = ctrl.Rule(qualidade_servico["mais ou menos"], porcentagem_gorjeta["média"])
regra_3 = ctrl.Rule(
    qualidade_servico["ruim"] & qualidade_comida["horrível"],
    porcentagem_gorjeta["baixa"],
)

gorjeta_ctrl = ctrl.ControlSystem([regra_1, regra_2, regra_3])
simulador = ctrl.ControlSystemSimulation(gorjeta_ctrl)

# Entrando com alguns valores para qualidade da comida e do serviço
simulador.input["comida"] = 3.5
simulador.input["servico"] = 9.5

# valor total da conta, sem a gorjeta
valor_conta = 200.0

# Computando o resultado
simulador.compute()
valor_gorjeta = valor_conta * (simulador.output["gorjeta"]/100)
print("Valor da conta sem a gorjeta: {:.2f}".format(valor_conta))
print("Porcentagem da gorjeta: {:.2f}".format(simulador.output["gorjeta"]))

print("valor da gorjeta: {:.2f}".format(valor_gorjeta))
print("valor total da conta com gorjeta: {:.2f}".format(valor_conta + valor_gorjeta))

# Mostrando o gráfico da gorjeta (tem hora que funciona no repl.it, outras não)
porcentagem_gorjeta.view(sim=simulador)

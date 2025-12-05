'''
Завдання 1. Оптимізація виробництва

Компанія виробляє два види напоїв: "Лимонад" і "Фруктовий сік". 
Для виробництва цих напоїв використовуються різні інгредієнти та обмежена кількість обладнання. 
Задача полягає у максимізації виробництва, враховуючи обмежені ресурси.

Умови завдання:
1. "Лимонад" виготовляється з "Води", "Цукру" та "Лимонного соку".
2. "Фруктовий сік" виготовляється з "Фруктового пюре" та "Води".
3. Обмеження ресурсів: 100 од. "Води", 50 од. "Цукру", 30 од. "Лимонного соку" та 40 од. "Фруктового пюре".
4. Виробництво одиниці "Лимонаду" вимагає 2 од. "Води", 1 од. "Цукру" та 1 од. "Лимонного соку".
5. Виробництво одиниці "Фруктового соку" вимагає 2 од. "Фруктового пюре" та 1 од. "Води".

Використовуючи PuLP, створіть модель, яка визначає, скільки "Лимонаду" та "Фруктового соку" 
потрібно виробити для максимізації загальної кількості продуктів, дотримуючись обмежень на ресурси. 
Напишіть програму, код якої максимізує загальну кількість вироблених продуктів "Лимонад" та "Фруктовий сік", 
враховуючи обмеження на кількість ресурсів.
'''

import pulp

# Parameters

# resources quantity
WATER_QTY = 100
SUGAR_QTY = 50
CITRON_QTY = 30
FRUIT_QTY = 40
# production parameters
WATER_LIMO_PROD = 2
SUGAR_LIMO_PROD = 1
CITRON_LIMO_PROD = 1
FRUIT_JUICE_PROD = 2
WATER_JUICE_PROD = 1



def main():
    
    model = pulp.LpProblem("Maximize production quantity", pulp.LpMaximize)

    # Product variables
    lemo_qty = pulp.LpVariable("Lemo", lowBound=0, cat="Integer")
    juice_qty = pulp.LpVariable("Saft", lowBound=0, cat="Integer")

    # Target variable: production qty
    model += lemo_qty + juice_qty, "Total Production"

    # bounders    
    model += lemo_qty * WATER_LIMO_PROD + juice_qty * WATER_JUICE_PROD <= WATER_QTY # water
    model += lemo_qty * SUGAR_LIMO_PROD <= SUGAR_QTY                                # sugar
    model += lemo_qty * CITRON_LIMO_PROD <= CITRON_QTY                              # citron juice
    model += juice_qty * FRUIT_JUICE_PROD <= FRUIT_QTY                              # fruit pure

    # solving
    model.solve()

    # results    
    print("Статус вирішення:")
    if pulp.LpStatus[model.status] == 'Optimal':
        print(pulp.LpStatus[model.status])
        print("-"*50)
        print("Виробляти лимонаду:", lemo_qty.varValue)
        print("Виробляти фруктового соку:", juice_qty.varValue)
        total = lemo_qty.varValue + juice_qty.varValue
        print("Загальна кількість продуктів:", total)        
        print("-"*50)
        print("Залишки ресурсів:")
        water_rem = WATER_QTY - lemo_qty.varValue*WATER_LIMO_PROD - juice_qty.varValue*WATER_JUICE_PROD
        sugar_rem = SUGAR_QTY - lemo_qty.varValue*SUGAR_LIMO_PROD
        citron_rem = CITRON_QTY - lemo_qty.varValue*CITRON_LIMO_PROD
        fruit_rem = FRUIT_QTY - juice_qty.varValue*FRUIT_JUICE_PROD
        print(f"Води =              {water_rem}")
        print(f"Цукру =             {sugar_rem}")
        print(f"Лимонного соку =    {citron_rem}")
        print(f"Фруктового пюре =   {fruit_rem}")
    else:
        print("Розв'язок не знайдено!")    

if __name__ == "__main__":
    main()

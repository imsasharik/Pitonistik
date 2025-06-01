import numpy
import pandas as pd
import matplotlib.pyplot as plt


dt = pd.read_csv("company_sales_data.csv", sep=',')

ox = dt['month_number']
oy = dt['total_profit']

# task1
df = pd.read_csv('company_sales_data.csv')

plt.figure(figsize=(8, 5))
plt.plot(df['month_number'], df['total_profit'], linestyle='-', linewidth=2)
plt.xlabel('Номер месяца')
plt.ylabel('Общая прибыль')
plt.title('Общая прибыль по месяцам')
plt.grid(True)
plt.show()


# task2
plt.figure(figsize=(8, 5))
plt.plot(
    df['month_number'],
    df['total_units'],
    linestyle='--',
    color='red',
    marker='o',
    markerfacecolor = "Black",
    linewidth=3,
    label='Продажи'
)
plt.xlabel('Номер месяца')
plt.ylabel('Количество проданных единиц')
plt.title('Продажи по месяцам')
plt.legend(loc='lower right')
plt.grid(True)
plt.show()


# task3
for column in dt.columns:
    if "total" in column or "month" in column: continue
    oy = dt[column]
    plt.plot(ox,oy,'-o',label=column)
plt.title("Sales data")
plt.xlabel("Month number")
plt.ylabel("Sales unit in month")
plt.xticks(ox)
plt.legend()
plt.show()

fig, ax = plt.subplots(nrows=3, ncols= 2, sharex=True)

i = 0
for column in dt.columns:
    if "total" in column or "month" in column: continue
    oy = dt[column]
    ax[i%3,i%2].plot(ox, oy, '-o', c=numpy.random.rand(3,))
    ax[i%3,i%2].set_title(oy.name)
    i += 1
ax[1,0].set_ylabel("Sales units in number")
ax[2, 0].set_xlabel("Month number")
ax[2,1].set_xlabel("Month number")
plt.show()


# task4
ox = dt['month_number']
oy = dt['total_profit']

oy = dt['toothpaste']
plt.scatter(ox, oy)
plt.grid(True, linestyle='--')
plt.title("Tooth paste Sales data")
plt.ylabel("Number of units Sold")
plt.xlabel("Month Number")
plt.xticks(ox)
plt.legend(['toothpaste'])

plt.show()


# task5
import numpy as np

months = df['month_number']
bar_width = 0.35
x = np.arange(len(months))

plt.figure(figsize=(10, 6))
plt.bar(x - bar_width/2, df['facecream'], width=bar_width, label='Крем для лица')
plt.bar(x + bar_width/2, df['facewash'], width=bar_width, label='Пенка для умывания')
plt.xlabel('Номер месяца')
plt.ylabel('Продажи')
plt.title('Сравнение продаж')
plt.xticks(x, months)
plt.legend(loc='upper left')
plt.show()
plt.show()


# task6
products = ['facecream', 'facewash', 'toothpaste', 'bathingsoap', 'shampoo', 'moisturizer']
total_sales = df[products].sum()
plt.figure(figsize=(8, 8))
plt.pie(
    total_sales,
    labels=total_sales.index,
    autopct='%1.1f%%',
    startangle=90
)
plt.title('Доля продаж по продуктам за год')
plt.show()


# task7
dt_amounts = []
for column in dt.columns:
    if "total" in column or "month" in column: continue
    ar = []
    for i in range(12):
        ar.append(dt.loc[i, column])
    dt_amounts.append(np.int_(ar))

oy = np.vstack([x for x in dt_amounts])

fig, ax = plt.subplots()
ax.stackplot(ox, oy)
ax.set_ylabel('Sales units in Number')
ax.set_xlabel('Month Number')
ax.set_title('All product sales data using stack plot')
plt.legend(dt.columns[1:-2], loc='upper left')
plt.show()


#task8
plt.figure(figsize=(10, 6))

ax1 = plt.subplot2grid((2, 3), (0, 0), colspan=3)

ax2 = plt.subplot2grid((2, 3), (1, 0))
ax3 = plt.subplot2grid((2, 3), (1, 1))
ax4 = plt.subplot2grid((2, 3), (1, 2))

plt.show()
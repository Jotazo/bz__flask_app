from movements import app
from flask import render_template
import csv

@app.route('/')
def listaIngresos():
    fIngresos = open('movements/data/basededatos.csv', 'r')
    csvReader = csv.reader(fIngresos, delimiter=',', quotechar='"')    
    ingresos = list(csvReader)
    total = 0

    for ingreso in ingresos:
        total+= float(ingreso[2])

    
    return render_template('movementsList.html', datos=ingresos, total=total)

@app.route('/creaalta')
def nuevoIngreso():
    return 'Ya el miércoles...'
''' Data Parameter
-data_size: in Procent (wird später /100)

'''
model_params = {
    "dense_units":["dense_units_1",],
    "dense_units_1": 256,
    "activation_1": "relu",
    "use_batch_norm_1": True,
    "dense_units_2": 128,
    "activation_2": "relu",
    "use_batch_norm_2": True,
    "dense_units_3": 64,
    "output_units": 3,
    "learning_rate": 0.001,
    "epochs": 200,
    "batch_size": 32
}

''' Data Parameter
-data_size: in Procent (wird später /100)
-test_size: bestimmt den Anteil der Daten, der dem Testset zugewiesen wird (liegt bei 0.2-0.3)
-random_state: Zufallszahlengenerator oder ein fester Seed. Wenn denselbe Seed verwendet wird, ist bei jedem Durchlauf denselben Split der Daten [nützlich, da Ergebnisse reproduzierbar]


'''

data_params = {
    "data_size": 2,
    "test_size": 0.2,
    "random_state": 42
}
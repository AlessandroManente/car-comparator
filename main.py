import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import sys


class Auto:

    TIPO = ""

    def __init__(self, nome, eta):
        self.nome = nome
        self.eta = eta
        self.costo_cumulativo = []

    @property
    def costo_cumulativo(self):
        return self._costo_cumulativo

    @costo_cumulativo.setter
    def costo_cumulativo(self, val):
        self._costo_cumulativo = val

    def costi_carburanti_urbano_annuo(self):
        pass

    def costi_carburanti_extraurbano_annuo(self):
        pass

    def costi_carburanti_annui(self):
        pass

    def calcola_bollo(self):
        pass

    def calcola_costo_cumulativo(self, anni, dict_costi_attuali):
        pass

    def print_costo_cumulativo(self, anni, dict_costi_attuali):
        self._costo_cumulativo = self.calcola_costo_cumulativo(anni, dict_costi_attuali)
        print(
            self.nome.replace("_", " ") + ":",
            self._costo_cumulativo[-1],
        )


class BENZINA(Auto):

    TIPO = "BENZINA"

    def __init__(self, nome, eta, dict_dati):
        super().__init__(nome, eta)
        self.consumo_benzina_litro_urbano = dict_dati["consumo_benzina_litro_urbano"]
        self.consumo_benzina_litro_extraurbano = dict_dati[
            "consumo_benzina_litro_extraurbano"
        ]
        self.percentuale_urbano = dict_dati["percentuale_urbano"]
        self.potenza = dict_dati["potenza"]
        self.costo_iniziale = dict_dati["costo_iniziale"]
        self.costo_manutenzione = dict_dati["costo_manutenzione"]

    def costi_carburanti_urbano_annuo(self, dict_costi_attuali):
        return (
            dict_costi_attuali["km_annui"]
            * self.consumo_benzina_litro_urbano
            * dict_costi_attuali["costo_benzina"]
        )

    def costi_carburanti_extraurbano_annuo(self, dict_costi_attuali):
        return dict_costi_attuali["km_annui"] * (
            self.consumo_benzina_litro_extraurbano * dict_costi_attuali["costo_benzina"]
        )

    def costi_carburanti_annuo(self, dict_costi_attuali):
        return self.costi_carburanti_urbano_annuo(
            dict_costi_attuali
        ) * self.percentuale_urbano + self.costi_carburanti_extraurbano_annuo(
            dict_costi_attuali
        ) * (
            1 - self.percentuale_urbano
        )

    def calcola_bollo(self):
        return 0

    def calcola_costo_cumulativo(self, anni, dict_costi_attuali):
        costo_iniziale = self.costo_iniziale
        costo_carburanti_annuo = self.costi_carburanti_annuo(dict_costi_attuali)
        costo_bollo = self.calcola_bollo()
        costo_manutenzione = self.costo_manutenzione

        costi_per_anno = []
        costo_da_aggiungere = costo_iniziale
        for anno in range(1, anni + 1):
            costo_da_aggiungere += costo_carburanti_annuo
            costo_da_aggiungere += costo_bollo
            costo_da_aggiungere += costo_manutenzione
            costi_per_anno.append(round(costo_da_aggiungere, 2))

        return costi_per_anno


class GPL(Auto):

    TIPO = "GPL"

    def __init__(self, nome, eta, dict_dati):
        super().__init__(nome, eta)
        self.consumo_gpl_litro_urbano = dict_dati["consumo_gpl_litro_urbano"]
        self.consumo_benzina_litro_urbano = dict_dati["consumo_benzina_litro_urbano"]
        self.consumo_gpl_litro_extraurbano = dict_dati["consumo_gpl_litro_extraurbano"]
        self.consumo_benzina_litro_extraurbano = dict_dati[
            "consumo_benzina_litro_extraurbano"
        ]
        self.percentuale_gpl = dict_dati["percentuale_gpl"]
        self.percentuale_urbano = dict_dati["percentuale_urbano"]
        self.potenza = dict_dati["potenza"]
        self.costo_iniziale = dict_dati["costo_iniziale"]
        self.costo_manutenzione = dict_dati["costo_manutenzione"]

    def costi_carburanti_urbano_annuo(self, dict_costi_attuali):
        costo_gpl_km_urbano = (
            self.consumo_gpl_litro_urbano
            * self.percentuale_gpl
            * dict_costi_attuali["costo_gpl"]
        )
        costo_benzina_km_urbano = (
            self.consumo_benzina_litro_urbano
            * (1 - self.percentuale_gpl)
            * dict_costi_attuali["costo_benzina"]
        )
        return dict_costi_attuali["km_annui"] * (
            costo_gpl_km_urbano + costo_benzina_km_urbano
        )

    def costi_carburanti_extraurbano_annuo(self, dict_costi_attuali):
        costo_gpl_km_extraurbano = (
            self.consumo_gpl_litro_extraurbano
            * self.percentuale_gpl
            * dict_costi_attuali["costo_gpl"]
        )
        costo_benzina_km_extraurbano = (
            self.consumo_benzina_litro_extraurbano
            * (1 - self.percentuale_gpl)
            * dict_costi_attuali["costo_benzina"]
        )
        return dict_costi_attuali["km_annui"] * (
            costo_gpl_km_extraurbano + costo_benzina_km_extraurbano
        )

    def costi_carburanti_annuo(self, dict_costi_attuali):
        return self.costi_carburanti_urbano_annuo(
            dict_costi_attuali
        ) * self.percentuale_urbano + self.costi_carburanti_extraurbano_annuo(
            dict_costi_attuali
        ) * (
            1 - self.percentuale_urbano
        )

    def calcola_bollo(self):
        return self.potenza * 2.58 * 0.25

    def calcola_costo_cumulativo(self, anni, dict_costi_attuali):
        costo_iniziale = self.costo_iniziale
        costo_carburanti_annuo = self.costi_carburanti_annuo(dict_costi_attuali)
        costo_bollo = self.calcola_bollo()
        costo_manutenzione = self.costo_manutenzione
        costo_cambio_bombola = int((anni + self.eta) / 10) * 500

        costi_per_anno = []
        costo_da_aggiungere = costo_iniziale
        for anno in range(1, anni + 1):
            costo_da_aggiungere += costo_carburanti_annuo
            costo_da_aggiungere += costo_bollo
            costo_da_aggiungere += costo_manutenzione
            if (anno + self.eta) % 10 == 0:
                costo_da_aggiungere += 500
            costi_per_anno.append(round(costo_da_aggiungere, 2))

        return costi_per_anno


def carica_auto_GPL(dati):
    auto_gpl = GPL(
        dati["nome"][0],
        float(dati["età"]),
        {
            "consumo_gpl_litro_urbano": float(dati["consumo_gpl_litro_urbano"]) / 100,
            "consumo_benzina_litro_urbano": float(dati["consumo_benzina_litro_urbano"])
            / 100,
            "consumo_gpl_litro_extraurbano": float(
                dati["consumo_gpl_litro_extraurbano"]
            )
            / 100,
            "consumo_benzina_litro_extraurbano": float(
                dati["consumo_benzina_litro_extraurbano"]
            )
            / 100,
            "percentuale_gpl": float(dati["percentuale_gpl"]),
            "percentuale_urbano": float(dati["percentuale_urbano"]),
            "potenza": float(dati["potenza"]),
            "costo_iniziale": float(dati["costo_iniziale"]),
            "costo_manutenzione": float(dati["costo_manutenzione"]),
        },
    )
    return auto_gpl


def carica_auto_BENZINA(dati):
    auto_benzina = BENZINA(
        dati["nome"][0],
        float(dati["età"]),
        {
            "consumo_benzina_litro_urbano": float(dati["consumo_benzina_litro_urbano"])
            / 100,
            "consumo_benzina_litro_extraurbano": float(
                dati["consumo_benzina_litro_extraurbano"]
            )
            / 100,
            "percentuale_urbano": float(dati["percentuale_urbano"]),
            "potenza": float(dati["potenza"]),
            "costo_iniziale": float(dati["costo_iniziale"]),
            "costo_manutenzione": float(dati["costo_manutenzione"]),
        },
    )
    return auto_benzina


def compara_due_auto(auto_1, auto_2, anni, dati_auto_1, dati_auto_2):
    auto_1.print_costo_cumulativo(anni, dati_auto_1)
    auto_2.print_costo_cumulativo(anni, dati_auto_2)

    fig, ax = plt.subplots()
    x = np.array(list(range(1, anni + 1)))
    y_1 = np.array(auto_1.costo_cumulativo)
    y_2 = np.array(auto_2.costo_cumulativo)
    ax.plot(
        x,
        y_1,
        label=auto_1.nome,
    )
    ax.plot(
        x,
        y_2,
        label=auto_2.nome,
    )
    trans = transforms.blended_transform_factory(
    ax.get_yticklabels()[0].get_transform(), ax.transData)
    ax.text(0,y_1[0], "{:.0f}".format(y_1[0]), color="red", transform=trans, 
        ha="right", va="center")
    ax.text(0,y_1[-1], "{:.0f}".format(y_1[-1]), color="red", transform=trans, 
        ha="right", va="center")
    ax.text(0,y_2[0], "{:.0f}".format(y_2[0]), color="blue", transform=trans, 
        ha="right", va="center")
    ax.text(0,y_2[-1], "{:.0f}".format(y_2[-1]), color="blue", transform=trans, 
        ha="right", va="center")
    ax.set_xticks(x)
    plt.show()


def annot_max(x, y, ax=None):
    xmax = x[np.argmax(y)]
    ymax = y.max()
    text = "x={:.3f}, y={:.3f}".format(xmax, ymax)
    if not ax:
        ax = plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops = dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=60")
    kw = dict(
        xycoords="data",
        textcoords="axes fraction",
        arrowprops=arrowprops,
        bbox=bbox_props,
        ha="right",
        va="top",
    )
    ax.annotate(text, xy=(xmax, ymax), xytext=(0.94, 0.96), **kw)


# if __name__ == "__main__":
#     COSTO_GPL = 0.809
#     COSTO_BENZINA = 1.769
#     KM_ANNUI = 12000
#     ANNI = 20

#     data = pd.read_csv("data\car_database.csv")
#     sandero_csv = data[data["nome"] == "Sandero_Streetway_2021"].reset_index()
#     sandero_streetway = carica_auto_GPL(sandero_csv)

#     cross_csv = data[data["nome"] == "Toyota_Yaris_Cross_2022"].reset_index()
#     toyota_yaris_cross = carica_auto_BENZINA(cross_csv)

#     compara_due_auto(
#         sandero_streetway,
#         toyota_yaris_cross,
#         ANNI,
#         {"km_annui": KM_ANNUI, "costo_gpl": COSTO_GPL, "costo_benzina": COSTO_BENZINA},
#         {"km_annui": KM_ANNUI, "costo_benzina": COSTO_BENZINA},
#     )
#     pass

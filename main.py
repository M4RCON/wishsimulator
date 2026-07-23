import random
import sys

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

mochileiro = ["Qiqi", "Dehya", "Yumemizuki Mizuki", "Tighnari", "Mona", "Keqing", "Jean", "Diluc"]
limitado = ["Sandrone", "Citlali", "Columbina", "Raiden Shogun"]
quatroestrelas = ["Aino", "Amber", "Barbara", "Beidou", "Bennett", "Candace", "Charlotte", "Chevreuse", "Chongyun", "Collei", "Dahlia", "Diona", "Dori", "Faruzan", "Fischl", "Freminet", "Gaming", "Gorou", "Iansan", "Ifa", "Illuga", "Jahoda", "Kachina", "Kaeya", "Kaveh", "Kirara", "Kujou Sara", "Kuki Shinobu", "Lan Yan", "Layla", "Lisa", "Lynette", "Mika", "Ningguang", "Noelle", "Ororon", "Prune", "Razor", "Rosaria", "Sayu", "Sethos", "Shikanoin Heizou", "Sucrose", "Thoma", "Xiangling", "Xingqiu", "Xinyan", "Yanfei", "Yaoyao", "Yun Jin"]
armatresstars = ["Messenger", "Raven Bow", "Recurve Bow", "Sharpshooter's Oath", "Slingshot", "Emerald Orb", "Magic Guide", "Otherworldly Story", "Thrilling Tales of Dragon Slayers", "Twin Nephrite", "Bloodtainted Greatsword", "Debate Club", "Ferrous Shadow", "Skyrider Greatsword", "White Iron Greatsword", "Black Tassel", "Halberd", "White Tassel", "Cool Steel", "Dark Iron Sword", "Fillet Blade", "Harbinger of Dawn", "Skyrider Sword", "Traveler's Handy Sword"]

STAR_SYMBOL = {5: "⭐⭐⭐⭐⭐", 4: "⭐⭐⭐⭐", 3: "⭐⭐⭐"}


def chance_cinco(pity):
    if pity >= 90:
        return 1.0
    if pity >= 74:
        return 0.006 + 0.06 * (pity - 73)
    return 0.006


def chance_quatro(pity):
    if pity >= 10:
        return 1.0
    if pity == 9:
        return 0.551
    return 0.051

def escolher_limitado():
    print("\nPersonagens disponiveis no banner limitado:")
    for i, nome in enumerate(limitado, start=1):
        print(f"{i} - {nome}")

    while True:
        raw = input("Em qual personagem você quer atirar? (número): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(limitado):
            return limitado[int(raw) - 1]
        print(f"Por favor, digite um número entre 1 e {len(limitado)}.")


def desejos(state, personagem_limitado):
    state["pity5"] += 1
    state["pity4"] += 1

    if random.random() < chance_cinco(state["pity5"]):
        pity_used = state["pity5"]
        state["pity5"] = 0
        state["pity4"] = 0
        if state["guaranteed5"] or random.random() < 0.5:
            item = personagem_limitado
            banner_type = "Limitado"
            state["guaranteed5"] = False
        else:
            item = random.choice(mochileiro)
            banner_type = "Standard"
            state["guaranteed5"] = True
        return 5, item, pity_used, banner_type

    if random.random() < chance_quatro(state["pity4"]):
        state["pity4"] = 0
        return 4, random.choice(quatroestrelas), None, None

    return 3, random.choice(armatresstars), None, None


def cont_desejos():
    while True:
        raw = input("Quantos desejos você quer fazer (máx. 10)? ").strip()
        if raw.isdigit() and 0 < int(raw) <= 10:
            return int(raw)
        print("Por favor, digite um número inteiro entre 1 e 10.")


def main():
    state = {"pity5": 0, "pity4": 0, "guaranteed5": False}
    counts = {5: 0, 4: 0, 3: 0}
    five_star_log = []

    personagem_limitado = escolher_limitado()
    print(f"\nVocê está atirando em: {personagem_limitado}\n")

    wish_number = 0
    got_limited_five_star = False
    while not got_limited_five_star:
        batch_size = cont_desejos()
        for _ in range(batch_size):
            wish_number += 1
            rarity, item, pity_used, banner_type = desejos(state, personagem_limitado)
            counts[rarity] += 1
            print(STAR_SYMBOL[rarity], item)

            if rarity == 5:
                five_star_log.append({
                    "Desejo Nº": wish_number,
                    "Personagem/Item": item,
                    "Tipo": banner_type,
                    "Pity": pity_used,
                })
                if banner_type == "Limitado":
                    got_limited_five_star = True
                    break

    print("\n--- Resumo ---")
    print(f"5 estrelas: {counts[5]}")
    print(f"4 estrelas: {counts[4]}")
    print(f"3 estrelas: {counts[3]}")

    if five_star_log:
        df = pd.DataFrame(five_star_log)
        df.to_excel("pity_5estrelas.xlsx", index=False)
        print("\nPlanilha 'pity_5estrelas.xlsx' gerada com o histórico de 5★.")
    else:
        print("\nNenhum 5★ obtido, nenhuma planilha foi gerada.")


if __name__ == "__main__":
    main()
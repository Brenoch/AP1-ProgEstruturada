import random

# Operações do aventureiro
def aventureiro_andar(aventureiro, direcao):
    movimento = {"W": [0, -1], "A": [-1, 0], "S": [0, 1], "D": [1, 0]}.get(direcao)
    nova_posicao = [aventureiro["posicao"][0] + movimento[0], aventureiro["posicao"][1] + movimento[1]]
    if posicao_valida(nova_posicao):
        aventureiro["posicao"] = nova_posicao
        return True
    return False

def aventureiro_atacar(aventureiro):
    return aventureiro["forca"] + random.randint(1, 6)

def aventureiro_defender(aventureiro, dano):
    dano_absorvido = max(0, dano - aventureiro["defesa"])
    aventureiro["vida"] -= dano_absorvido

def ver_atributos_aventureiro(aventureiro):
    print(f"Atributos do aventureiro {aventureiro['nome']}:")
    print(f"Força: {aventureiro['forca']}")
    print(f"Defesa: {aventureiro['defesa']}")
    print(f"Vida: {aventureiro['vida']}")

def aventureiro_esta_vivo(aventureiro):
    return aventureiro["vida"] > 0

# Operações do monstro
def novo_monstro():
    print("Um novo monstro apareceu!")
    return {
        "forca": random.randint(5, 25),
        "vida": random.randint(10, 100)
    }

def monstro_atacar(monstro):
    return monstro["forca"]

def monstro_defender(monstro, dano):
    monstro["vida"] -= dano

def monstro_esta_vivo(monstro):
    return monstro["vida"] > 0

# Operações do mapa
def desenhar(aventureiro, tesouro):
    for y in range(10):
        for x in range(10):
            if [x, y] == aventureiro["posicao"]:
                print("@", end=" ")
            elif [x, y] == tesouro:
                print("X", end=" ")
            else:
                print(".", end=" ")
        print()

# Combate
def iniciar_combate(aventureiro, monstro):
    print("Combate iniciado!")
    while aventureiro_esta_vivo(aventureiro) and monstro_esta_vivo(monstro):
        # Fase do aventureiro
        dano_aventureiro = aventureiro_atacar(aventureiro)
        monstro_defender(monstro, dano_aventureiro)
        print(f"Você causou {dano_aventureiro} de dano ao monstro. Vida atual do monstro: {monstro['vida']}")

        # Verifica se o monstro foi derrotado
        if not monstro_esta_vivo(monstro):
            print("Você derrotou o monstro!")
            return True

        # Fase do monstro
        dano_monstro = monstro_atacar(monstro)
        aventureiro_defender(aventureiro, dano_monstro)
        print(f"O monstro causou {dano_monstro} de dano a você. Sua vida atual: {aventureiro['vida']}")

        # Verifica se o aventureiro foi derrotado
        if not aventureiro_esta_vivo(aventureiro):
            print("Você foi derrotado pelo monstro...")
            return False

# Operação principal do jogo
def movimentar(aventureiro, direcao):
    if not aventureiro_andar(aventureiro, direcao):
        return True

    efeito = random.choices(["nada", "monstro"], [0.6, 0.4])[0]
    if efeito == "monstro":
        monstro = novo_monstro()
        return iniciar_combate(aventureiro, monstro)

    return True

def gerar_tesouro():
    while True:
        tesouro = [random.randint(1, 9), random.randint(1, 9)]
        if tesouro != [0, 0]:
            return tesouro

def posicao_valida(posicao):
    x, y = posicao
    return 0 <= x < 10 and 0 <= y < 10

def main():

    aventureiro = {
        "nome": input("Deseja buscar um tesouro? Primeiro, informe seu nome: "),
        "forca": random.randint(10, 18),
        "defesa": random.randint(10, 18),
        "vida": random.randint(100, 120),
        "posicao": [0, 0]
    }
    print(f"Saudações, {aventureiro['nome']}! Boa sorte! ")

    tesouro = gerar_tesouro()
    print(f"Olá, {aventureiro['nome']}! Boa sorte na sua jornada!")

    while True:
        print("\nMapa:")
        desenhar(aventureiro, tesouro)

        comando = input("\nDigite um comando (W/A/S/D para mover, T para atributos, Q para sair): ").upper()

        if comando == "Q":
            print("Fim do jogo.")
            break
        elif comando == "T":
            ver_atributos_aventureiro(aventureiro)
        elif comando in ["W", "A", "S", "D"]:
            if not movimentar(aventureiro, comando):
                print("Game over...")
                break
            if aventureiro["posicao"] == tesouro:
                print("Parabéns! Você encontrou o tesouro!")
                break
        else:
            print("Comando inválido!")

if __name__ == "__main__":
    main()
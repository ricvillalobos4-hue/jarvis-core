from core.brain import JarvisBrain


def main():
    print("\n" + "=" * 45)
    print("       J.A.R.V.I.S CORE")
    print("       SYSTEM ONLINE")
    print("       PROJECT BY KERENS<3")
    print("=" * 45)

    try:
        jarvis = JarvisBrain()
        print("\nJARVIS: Hola, Kerens. Estoy listo para ayudarte.")

        while True:
            message = input("\nKERENS: ").strip()

            if message.lower() in ("salir", "exit", "cerrar"):
                print("\nJARVIS: Hasta pronto.")
                break

            if not message:
                continue

            try:
                response = jarvis.think(message)
                print(f"\nJARVIS: {response}")

            except Exception as error:
                print(f"\nJARVIS: Error: {error}")

    except KeyboardInterrupt:
        print("\nJARVIS: Sistema desconectado.")

    except Exception as error:
        print(f"\nError al iniciar JARVIS: {error}")


if __name__ == "__main__":
    main()

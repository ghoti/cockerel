import os

def main():
    import asyncio

    alive = True

    while alive:
        from cockerel import Cockerel
        c = None
        try:
            c = Cockerel()
            print('Starting up', flush=True)
            c.run()
        except Exception as e:
            print(e.message)
            os._exit(0)
            break
        finally:
            if not c or c.ok:
                break

if __name__ == '__main__':
    main()
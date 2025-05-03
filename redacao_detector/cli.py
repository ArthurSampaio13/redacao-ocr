import argparse
from rich.console import Console
from rich.panel import Panel
from redacao_detector import processar_imagem, processar_diretorio

console = Console()


def welcome_banner():
    print(
        """
    ██████╗ ███████╗██████╗  █████╗  ██████╗ █████╗  ██████╗       ██████╗ ███████╗████████╗███████╗ ██████╗████████╗ ██████╗ ██████╗ 
    ██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔═══██╗      ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
    ██████╔╝█████╗  ██║  ██║███████║██║     ███████║██║   ██║█████╗██║  ██║█████╗     ██║   █████╗  ██║        ██║   ██║   ██║██████╔╝
    ██╔══██╗██╔══╝  ██║  ██║██╔══██║██║     ██╔══██║██║   ██║╚════╝██║  ██║██╔══╝     ██║   ██╔══╝  ██║        ██║   ██║   ██║██╔══██╗
    ██║  ██║███████╗██████╔╝██║  ██║╚██████╗██║  ██║╚██████╔╝      ██████╔╝███████╗   ██║   ███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║
    ╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝       ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
                                                                                                                                  
    """
    )


def main():
    welcome_banner()
    parser = argparse.ArgumentParser(
        description="📝 Detector de áreas de texto em imagens de redação"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--imagem", "-i", help="Caminho para uma imagem única a ser processada"
    )
    group.add_argument(
        "--diretorio",
        "-d",
        help="Caminho para um diretório contendo imagens a serem processadas",
    )

    parser.add_argument(
        "--saida",
        "-o",
        help="Diretório onde os resultados serão salvos (padrão: mesmo diretório da entrada)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Ativa o modo de depuração e salva imagens intermediárias",
    )
    parser.add_argument(
        "--nao-salvar",
        action="store_true",
        help="Não salva os resultados das imagens processadas",
    )

    args = parser.parse_args()

    if args.imagem:
        console.rule("[bold cyan]Processamento de Imagem Única")
        console.print(f"[bold green]Imagem:[/] {args.imagem}")
        try:
            resultado = processar_imagem(
                args.imagem,
                salvar_resultado=not args.nao_salvar,
                mostrar_debug=args.debug,
            )

            if isinstance(resultado, tuple):
                console.print(
                    Panel.fit("✅ Imagem processada com debug!", style="bold yellow")
                )
            else:
                console.print(
                    Panel.fit(
                        f"✅ Resultado salvo em:\n[bold blue]{resultado}",
                        style="bold green",
                    )
                )

        except Exception as e:
            console.print(
                Panel.fit(f"❌ Erro ao processar a imagem:\n{e}", style="bold red")
            )

    elif args.diretorio:
        console.rule("[bold cyan]Processamento em Lote")
        console.print(f"[bold green]Diretório:[/] {args.diretorio}")
        try:
            processar_diretorio(args.diretorio, diretorio_saida=args.saida, params=None)
            console.print(Panel.fit("✅ Processamento concluído!", style="bold green"))
        except Exception as e:
            console.print(
                Panel.fit(f"❌ Erro ao processar diretório:\n{e}", style="bold red")
            )


if __name__ == "__main__":
    main()

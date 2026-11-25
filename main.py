import json
import os
import flet as ft

ARQUIVO_ESTOQUE = "estoque_papelaria.json"


# --- FUNÇÕES PARA GRAVAR E LER O ARQUIVO JSON ---
def carregar_estoque():
    if os.path.exists(ARQUIVO_ESTOQUE):
        with open(ARQUIVO_ESTOQUE, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    return []


def salvar_estoque(itens):
    with open(ARQUIVO_ESTOQUE, "w", encoding="utf-8") as arquivo:
        json.dump(itens, arquivo, indent=4, ensure_ascii=False)


# --- APLICATIVO PRINCIPAL ---
def main(page: ft.Page):
    page.title = "Controle de Estoque - Papelaria"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.GREY_50
    page.window.width = 800
    page.window.height = 680
    page.padding = 25
    page.scroll = ft.ScrollMode.AUTO

    estoque = carregar_estoque()
    indice_edicao = None

    # Campos de entrada personalizados para papelaria
    campo_nome = ft.TextField(
        label="Item de Papelaria (ex: Caderno 10 Matérias)",
        expand=True,
        bgcolor=ft.Colors.WHITE,
    )
    campo_marca = ft.TextField(
        label="Marca (ex: Tilibra, Faber-Castell, BIC)",
        width=250,
        bgcolor=ft.Colors.WHITE,
    )
    campo_categoria = ft.TextField(
        label="Categoria (ex: Escrita, Cadernos, Artes)",
        expand=True,
        bgcolor=ft.Colors.WHITE,
    )
    campo_preco = ft.TextField(
        label="Preço Unitário (R$)",
        width=180,
        bgcolor=ft.Colors.WHITE,
    )
    campo_qtd = ft.TextField(
        label="Qtd. em Estoque",
        width=160,
        bgcolor=ft.Colors.WHITE,
    )

    texto_aviso = ft.Text("", color=ft.Colors.RED_700, weight=ft.FontWeight.W_500)
    texto_resumo = ft.Text("", size=14, color=ft.Colors.TEAL_800, weight=ft.FontWeight.BOLD)
    lista_itens = ft.Column(spacing=10)

    def limpar_campos():
        nonlocal indice_edicao
        campo_nome.value = ""
        campo_marca.value = ""
        campo_categoria.value = ""
        campo_preco.value = ""
        campo_qtd.value = ""
        texto_aviso.value = ""
        indice_edicao = None
        btn_salvar.content = "Adicionar ao Estoque"
        btn_salvar.icon = ft.Icons.ADD_BOX
        btn_cancelar.visible = False

    # READ (Ler e mostrar os produtos na tela)
    def atualizar_tela():
        lista_itens.controls.clear()
        texto_resumo.value = f"Total de produtos diferentes cadastrados: {len(estoque)}"

        if not estoque:
            lista_itens.controls.append(
                ft.Container(
                    padding=20,
                    content=ft.Text(
                        "Nenhum material cadastrado no estoque da papelaria ainda.",
                        italic=True,
                        color=ft.Colors.GREY_600,
                    ),
                )
            )
        else:
            for idx, item in enumerate(estoque):
                cartao = ft.Card(
                    elevation=2,
                    content=ft.Container(
                        padding=15,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=8,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(
                                    spacing=4,
                                    controls=[
                                        ft.Text(
                                            f"{item['nome']} — {item['marca']}",
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.TEAL_900,
                                        ),
                                        ft.Text(
                                            f"Categoria: {item['categoria']}  |  Valor: R$ {item['preco']}  |  Disponível: {item['quantidade']} un.",
                                            size=14,
                                            color=ft.Colors.GREY_700,
                                        ),
                                    ],
                                ),
                                ft.Row(
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT_NOTE,
                                            icon_color=ft.Colors.AMBER_800,
                                            tooltip="Editar item",
                                            on_click=lambda e, i=idx: iniciar_edicao(i),
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE_OUTLINE,
                                            icon_color=ft.Colors.RED_700,
                                            tooltip="Remover do estoque",
                                            on_click=lambda e, i=idx: deletar_item(i),
                                        ),
                                    ]
                                ),
                            ],
                        ),
                    ),
                )
                lista_itens.controls.append(cartao)

        page.update()

    # CREATE e UPDATE (Criar novo ou atualizar existente)
    def salvar_item(e):
        nonlocal indice_edicao

        nome = campo_nome.value.strip()
        marca = campo_marca.value.strip()
        categoria = campo_categoria.value.strip()
        preco = campo_preco.value.strip()
        qtd = campo_qtd.value.strip()

        if not nome or not preco or not qtd:
            texto_aviso.value = "Por favor, preencha o Nome, o Preço e a Quantidade."
            page.update()
            return

        registro = {
            "nome": nome,
            "marca": marca if marca else "Sem marca",
            "categoria": categoria if categoria else "Papelaria Geral",
            "preco": preco,
            "quantidade": qtd,
        }

        if indice_edicao is None:
            estoque.append(registro)  # Create
        else:
            estoque[indice_edicao] = registro  # Update

        salvar_estoque(estoque)
        limpar_campos()
        atualizar_tela()

    def iniciar_edicao(idx):
        nonlocal indice_edicao
        item = estoque[idx]
        campo_nome.value = item["nome"]
        campo_marca.value = item["marca"]
        campo_categoria.value = item["categoria"]
        campo_preco.value = item["preco"]
        campo_qtd.value = item["quantidade"]

        indice_edicao = idx
        btn_salvar.content = "Atualizar Item"
        btn_salvar.icon = ft.Icons.CHECK_CIRCLE
        btn_cancelar.visible = True
        texto_aviso.value = ""
        page.update()

    # DELETE (Remover item)
    def deletar_item(idx):
        estoque.pop(idx)
        salvar_estoque(estoque)
        if indice_edicao == idx:
            limpar_campos()
        atualizar_tela()

    btn_salvar = ft.Button(
        content="Adicionar ao Estoque",
        icon=ft.Icons.ADD_BOX,
        bgcolor=ft.Colors.TEAL_700,
        color=ft.Colors.WHITE,
        on_click=salvar_item,
    )

    btn_cancelar = ft.Button(
        content="Cancelar",
        icon=ft.Icons.CLOSE,
        visible=False,
        on_click=lambda e: (limpar_campos(), atualizar_tela()),
    )

    # Estrutura visual da página
    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.STOREFRONT, size=34, color=ft.Colors.TEAL_700),
                        ft.Text(
                            "Estoque de Papelaria",
                            size=26,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.TEAL_900,
                        ),
                    ]
                ),
                texto_resumo,
            ],
        ),
        ft.Divider(color=ft.Colors.TEAL_200),
        ft.Row(controls=[campo_nome, campo_marca]),
        ft.Row(controls=[campo_categoria, campo_preco, campo_qtd]),
        ft.Row(controls=[btn_salvar, btn_cancelar, texto_aviso]),
        ft.Divider(color=ft.Colors.TEAL_200),
        ft.Text("Materiais em Estoque", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
        lista_itens,
    )

    atualizar_tela()


ft.run(main)
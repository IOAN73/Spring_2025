from asyncio import to_thread, create_task, Task
from dataclasses import dataclass
from pathlib import Path

from nicegui import ui, app


from knowlege_manage.file_utils import (
    create_directory,
    create_file,
    delete_file,
    file_read,
    file_write,
    get_nodes,
    rename_file,
)

DOCS_ADDRESS = 'http://localhost:80/mysite'

BTN_PROPS = 'color="teal-9"'
BTN_CLASS = 'hover:animate-pulse'

BASE_FOLDER = Path.cwd() / 'documentation' / 'docs'


@dataclass
class Data:
    filename: str
    text: str


@ui.page('/')
async def index():
    ui.open('http://localhost:80')


@ui.page('/edit')
async def main_page():
    ui.page_title('База знаний')

    def write_data(e):
        data.filename = str(e.value)
        data.text = file_read(BASE_FOLDER / e.value)

    def update_tree():
        tree._props['nodes'] = get_nodes(BASE_FOLDER)
        tree.update()

    def create_dialog():
        with (ui.dialog() as dialog, ui.card(), ui.column().classes('w-96')):
            file_name = ui.input(label='имя файла').classes('w-full')
            ui.button(
                text='создать файл',
                on_click=lambda: (
                    create_file(BASE_FOLDER / file_name.value),
                    ui.notify('Файл создан'),
                    dialog.close(),
                    update_tree(),
                ),
            ).classes('bg-teal-10')

            ui.button('Закрыть', on_click=dialog.close).classes(
                'bg-teal-10')
        dialog.open()

    def directory_dialog():
        with ui.dialog() as dialog, ui.card(), ui.column().classes('w-96'):
            folder_name = ui.input(label='имя папки').classes('w-full')
            ui.button(
                text='создать папку',
                on_click=lambda: (
                    create_directory(BASE_FOLDER / folder_name.value),
                    ui.notify('Папка создана'),
                    dialog.close(),
                    update_tree(),
                ),
            ).classes('bg-teal-10')

            ui.button('Закрыть', on_click=dialog.close).classes(
                'bg-teal-10')
        dialog.open()

    def rename_dialog():
        with ui.dialog() as dialog, ui.card(), ui.column().classes('w-96'):
            old_name = ui.input(label='старое имя файла').props(
                'readonly').classes('w-full')
            new_name = ui.input(label='новое имя файла').classes('w-full')
            ui.button(
                text='переименовать',
                on_click=lambda: (
                    rename_file(BASE_FOLDER / old_name.value, BASE_FOLDER / new_name.value),
                    ui.notify('Файл переименован'),
                    dialog.close(),
                    update_tree(),
                ),
            ).classes('bg-teal-10')
            ui.button('Закрыть', on_click=dialog.close).classes(
                'bg-teal-10')

        old_name.bind_value_from(data, 'filename')
        dialog.open()

    def save_foo():
        file_write(BASE_FOLDER / data.filename, data.text)
        ui.notify(f'сохранил {data.filename}')

    def delete_dialog():
        with ui.dialog() as dialog, ui.card(), ui.column().classes('w-96'):
            ui.label('Вы уверены что хотите удалить ?')
            ui.button(
                text='ДА',
                on_click=lambda: (
                    delete_file(BASE_FOLDER / data.filename),
                    ui.notify(f'Удален {data.filename}'),
                    dialog.close(),
                    update_tree(),
                ),
            ).classes('bg-teal-10')

            ui.button(text='НЕТ', on_click=lambda: dialog.close()).classes(
                'bg-teal-10')

        dialog.open()

    # Инициализация графики
    with ui.header(elevated=True).classes(replace='row items-center'):
        with ui.row().classes('w-full bg-teal-10 items-center q-pa-sm'):
            ui.button(
                on_click=lambda: left_drawer.toggle(),
                icon='menu',
            ).props('flat color=white')
            ui.button(
                text='База знаний',
                icon='school',
                on_click=lambda: ui.open(DOCS_ADDRESS),
            ).props('dense flat color=white')
            ui.separator().props('vertical')
            with ui.button_group().props('flat'):
                ui.button(
                    text='Создать файл',
                    icon='add',
                    on_click=create_dialog,
                ).props(BTN_PROPS).classes(BTN_CLASS)
                ui.button(
                    text='Создать папку',
                    icon='add_box',
                    on_click=directory_dialog,
                ).props(BTN_PROPS).classes(BTN_CLASS)
                ui.button(
                    text='Переименовать',
                    icon='edit',
                    on_click=rename_dialog,
                ).props(BTN_PROPS).classes(BTN_CLASS)
                ui.button(
                    text='удалить',
                    icon='delete_outline',
                    on_click=delete_dialog,
                ).props(BTN_PROPS).classes(BTN_CLASS)
                ui.button(
                    text='Сохранить',
                    icon='save',
                    on_click=save_foo,
                ).props(BTN_PROPS).classes(BTN_CLASS)
                ui.button(
                    text='Предпросмотр',
                    icon='preview',
                    on_click=lambda: (
                        markdown.set_visibility(not markdown.visible),
                        editor.set_visibility(not editor.visible),
                    ),
                ).props(BTN_PROPS).classes(BTN_CLASS)

    with ui.footer(value=False).classes(
            'bg-teal-5') as footer, ui.row().classes(
        'content-center justify-center w-full'):
        ui.link(
            text='Cинтаксис написания MarkDown файлов',
            target='https://docs.aspose.com/html/ru/net/markdown-syntax/'
        ).classes('text-h5 text-white')

    with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
        ui.button(on_click=footer.toggle, icon='contact_support').props(
            'fab').classes('bg-teal-10')

    with (
            ui.left_drawer(elevated=True)
                    .classes('bg-teal-3')
                    .props('overlay')
    ) as left_drawer:
        tree = ui.tree(
            nodes=get_nodes(BASE_FOLDER),
            node_key='id',
            label_key='label',
            children_key='child',
            on_select=write_data,
        )

    with ui.row().classes('w-full justify-center'):
        with ui.row().classes('w-full max-w-screen-md'):
            filename = ui.label().classes('text-bold')
            editor = (
                ui.textarea()
                .props('outlined input-class="h-[80vh]" bg-color="white"')
                .classes('w-full h-96')
            )
            markdown = ui.markdown('').classes('w-full')

    # Логика
    data = Data('', '')
    filename.bind_text_from(data, 'filename')
    editor.bind_value(data, 'text')
    markdown.bind_content_from(editor, 'value')
    markdown.bind_content_to(data, 'text')
    markdown.set_visibility(False)


async def start_docs():
    from mkdocs.commands import serve
    await to_thread(
        serve.serve,
        config_file=str(Path.cwd() / 'documentation' / 'mkdocs.yml'),
        dev_addr='localhost:80',  # noqa
    )  # noqa


bg_tasks: list[Task] = []


async def on_startup():
    bg_tasks.append(create_task(start_docs))


async def on_shutdown():
    for task in bg_tasks:
        task.cancel()


app.on_startup(start_docs)
app.on_shutdown(on_shutdown)

ui.run(show=True, reload=False)

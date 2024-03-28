import flet as ft
import flet_form as ff


async def main(page: ft.Page):

    text = ft.Text(f"Valid: False")

    def on_validation_complete(e: ff.ValidationCompleteEvent):
        print(e)
        if e.valid:
            text.value = "Valid: True"
            text.update()
        else:
            text.value = "Valid: False"
            text.update()

    form = ff.Form(
        on_validation_complete=on_validation_complete,
        controls=[
            text,
            ft.Container(
                padding=10,
                bgcolor="lightgray",
                content=ff.TextField(  # Form auto-detect this as a FormField
                    label="Name",
                    rules=[ff.required],
                    on_change=lambda e: print(e),
                ),
            ),
            ff.TextField(
                label="Email",
                rules=[ff.required],
            ),
        ],
    )

    page.add(form)


app = ft.app(main, export_asgi_app=True)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8550,
        reload=True,
    )

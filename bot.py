import os
import zipfile
import tempfile
from PIL import Image

from splitter import split_zip, split_folder
from spicy import obtener_serie, obtener_capitulo
from downloader import descargar_capitulo

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "8699617127:AAEPvcgg9uuAc4KFJbdkj2cifK_yAtyoOXk"

CUT_HEIGHT = 10000


async def recibir_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = update.message.text.strip() if update.message.text else ""

    # BUSCAR SERIE SPICYSERIES
    if "spicyseries.com" in texto:

        await update.message.reply_text(
            "🔎 Analizando serie..."
        )

        try:

            datos = obtener_serie(texto)

            if datos:

                context.user_data["serie_slug"] = datos["slug"]

                keyboard = []

                for cap in datos["capitulos"][:25]:

                    keyboard.append(
                        [
                            InlineKeyboardButton(
                                f"Capítulo {cap['num']}",
                                callback_data=f"{datos['slug']}|{cap['slug']}"
                            )
                        ]
                    )

                await update.message.reply_text(
                    f"✅ Serie encontrada:\n\n"
                    f"{datos['titulo']}\n\n"
                    "Selecciona un capítulo:",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )

            else:

                await update.message.reply_text(
                    "❌ No pude leer esa serie."
                )

        except Exception as e:

            await update.message.reply_text(
                f"❌ Error leyendo serie:\n{e}"
            )


        return


async def seleccionar_capitulo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    serie_slug, cap_slug = query.data.split("|")

    await query.edit_message_text(
        "📥 Descargando capítulo..."
    )

    try:

        cap = obtener_capitulo(
            serie_slug,
            cap_slug
        )

        if not cap:

            await query.message.reply_text(
                "❌ No pude obtener ese capítulo."
            )

            return

        await query.message.reply_text(
            "⬇️ Descargando imágenes..."
        )

        descargar_capitulo(cap)

        carpeta = (
            f"downloads/{serie_slug}/{cap_slug}"
        )

        await query.message.reply_text(
            "✂️ Cortando imágenes..."
        )

        zip_generado = split_folder(
            carpeta,
            cap_slug
        )

        await query.message.reply_text(
            "📦 Enviando ZIP..."
        )

        with open(zip_generado, "rb") as archivo_zip:

            await query.message.reply_document(
                document=archivo_zip,
                filename=os.path.basename(zip_generado)
            )

        await query.message.reply_text(
            f"✅ Capítulo {cap_slug} enviado correctamente."
        )

        if os.path.exists(zip_generado):
            os.remove(zip_generado)

    except Exception as e:

        await query.message.reply_text(
            f"❌ Error procesando capítulo:\n{e}"
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📚 Envíame un enlace de spicyseries.com.\n\n"
        "Selecciona el capítulo que quieras y te enviaré el ZIP cortado automáticamente.\n\n"
        "También puedes enviarme un ZIP de imágenes para cortarlo."
    )

async def recibir_zip(update: Update, context: ContextTypes.DEFAULT_TYPE):

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    documento = update.message.document

    if not documento.file_name.lower().endswith(".zip"):

        await update.message.reply_text(
            "❌ Solo acepto archivos ZIP."
        )

        return

    archivo = await documento.get_file()

    ruta = os.path.join(
        "uploads",
        documento.file_name
    )

    await archivo.download_to_drive(
        ruta
    )

    if "cola_zip" not in context.user_data:
        context.user_data["cola_zip"] = []

    context.user_data["cola_zip"].append(
        (ruta, documento.file_name)
    )

    await update.message.reply_text(
        f"📥 {documento.file_name} agregado a la cola.\n"
        f"Pendientes: {len(context.user_data['cola_zip'])}"
    )

    if not context.user_data.get("procesando_zip", False):

        await procesar_cola(update, context)


async def procesar_cola(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["procesando_zip"] = True

    while context.user_data["cola_zip"]:

        ruta, nombre = context.user_data["cola_zip"].pop(0)

        salida = None

        try:

            await update.message.reply_text(
                f"✂️ Procesando {nombre}..."
            )

            salida = split_zip(ruta)

            await update.message.reply_text(
                "📦 Enviando ZIP..."
            )

            with open(salida, "rb") as archivo_zip:

                await update.message.reply_document(
                    document=archivo_zip,
                    filename=os.path.basename(salida)
                )

            await update.message.reply_text(
                f"✅ {nombre} procesado correctamente."
            )

        except Exception as e:

            await update.message.reply_text(
                f"❌ Error procesando {nombre}:\n{e}"
            )

        finally:

            try:

                if os.path.exists(ruta):
                    os.remove(ruta)

            except:
                pass

            try:

                if salida and os.path.exists(salida):
                    os.remove(salida)

            except:
                pass

            print(f"Procesado: {ruta}")

    context.user_data["procesando_zip"] = False


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(
    CommandHandler(
        "start",
        start
    )
)

app.add_handler(
    CallbackQueryHandler(
        seleccionar_capitulo
    )
)

app.add_handler(
    MessageHandler(
        filters.Document.ALL,
        recibir_zip
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        recibir_texto
    )
)

print(
    "Bot iniciado..."
)

app.run_polling()

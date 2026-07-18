[app]
title = Manga Splitter
package.name = mangasplitter
package.domain = org.manga

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,zip

version = 1.0

requirements = python3,kivy,pillow,plyer

orientation = portrait

fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b

presplash.color = #202020

[buildozer]
log_level = 2
warn_on_root = 1

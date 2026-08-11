[app]

title = Alumni Tutor AI
package.name = tutorapp
package.domain = org.alumnitutor

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json

version = 0.1.0

requirements = python3,kivy,google-genai,requests,urllib3,certifi

orientation = portrait
fullscreen = 1

android.permissions = INTERNET

android.api = 34
android.minapi = 21

android.archs = arm64-v8a

android.release_artifact = aab

p4a.bootstrap = sdl2


[buildozer]

log_level = 2
warn_on_root = 1

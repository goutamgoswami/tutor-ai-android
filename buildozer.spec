```ini
[app]

# Application
title = Alumni Tutor AI
package.name = tutorapp
package.domain = org.alumnitutor

# Source
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json

# Version
version = 0.1.0

# Python dependencies
requirements = python3,kivy,google-genai,requests,urllib3,certifi

# Display
orientation = portrait
fullscreen = 1

# Permissions
android.permissions = INTERNET

# Android
android.api = 34
android.minapi = 21
android.ndk_api = 21

# Architecture
android.archs = arm64-v8a

# Google Play requires an Android App Bundle
android.release_artifact = aab

# AndroidX
android.enable_androidx = True

# Python-for-Android
p4a.bootstrap = sdl2

# Do not use old support libraries
android.add_src =

# Version code
android.numeric_version = 1


[buildozer]

# Log level
log_level = 2

# Warning: do not change this to /tmp
warn_on_root = 1
```

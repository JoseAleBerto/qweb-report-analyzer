# Guía completa: GitHub + Odoo App Store

---

## PASO 1 — Instalar Git (si no lo tienes)

Abre PowerShell y ejecuta:
```powershell
git --version
```
Si dice algo como `git version 2.x.x` ya lo tienes. Si da error, descárgalo de https://git-scm.com/download/win e instálalo con opciones por defecto.

---

## PASO 2 — Configurar tu identidad en Git (solo la primera vez)

```powershell
git config --global user.name "Jose Bertorelli"
git config --global user.email "josealebertorelli@gmail.com"
```

---

## PASO 3 — Crear el repositorio en GitHub

1. Ve a **https://github.com/new**
2. Rellena así:
   - **Repository name:** `qweb-report-analyzer`
   - **Description:** `Free Odoo addon to analyze QWeb report view dependencies`
   - **Visibility:** ✅ Public
   - ❌ NO marques "Add a README file"
   - ❌ NO marques "Add .gitignore"
   - ❌ NO marques "Choose a license"
3. Clic en **Create repository**
4. GitHub te mostrará una página con instrucciones — **ignórala**, usaremos los comandos de abajo.

---

## PASO 4 — Abrir PowerShell en la carpeta correcta

**Opción A (más fácil):** Abre el Explorador de Windows, navega hasta:
```
C:\Users\JABERTORELLI\Documents\Trabajo Tareas JAL\ODOO ADDONS JOSE BERTORELLI\QWEB_ADDON\github-repo
```
Haz clic en la barra de dirección, escribe `powershell` y pulsa Enter. Se abre PowerShell ya en esa carpeta.

**Opción B:** Abre PowerShell y ejecuta:
```powershell
cd "C:\Users\JABERTORELLI\Documents\Trabajo Tareas JAL\ODOO ADDONS JOSE BERTORELLI\QWEB_ADDON\github-repo"
```

Verifica que estás en la carpeta correcta — debe mostrar los archivos del repo:
```powershell
dir
```
Deberías ver: `.gitignore`, `README.md`, `SETUP_GITHUB.md`, y la carpeta `qweb_report_analyzer`.

---

## PASO 5 — Subir rama 19.0

Copia y pega estos comandos **uno por uno** (no todos juntos):

```powershell
git init
```
```powershell
git add .
```
```powershell
git commit -m "Initial release - QWeb Report Analyzer v1.0.0 (free & open source)"
```
```powershell
git branch -M 19.0
```
```powershell
git remote add origin https://github.com/josebertorelli/qweb-report-analyzer.git
```
```powershell
git push -u origin 19.0
```

⚠️ **Al hacer el push**, GitHub te pedirá autenticarte:
- Se abrirá una ventana del navegador pidiendo que inicies sesión en GitHub
- Inicia sesión con tu cuenta de GitHub normalmente
- Autoriza el acceso y vuelve a PowerShell
- El push continuará automáticamente

---

## PASO 6 — Crear rama 18.0

```powershell
git checkout -b 18.0
```

Ahora abre el archivo `qweb_report_analyzer\__manifest__.py` con el Bloc de Notas o VS Code y cambia **solo esta línea**:
```python
'version': '19.0.1.0.0',
```
por:
```python
'version': '18.0.1.0.0',
```
Guarda el archivo y vuelve a PowerShell:

```powershell
git add qweb_report_analyzer/__manifest__.py
```
```powershell
git commit -m "Branch 18.0 - initial release"
```
```powershell
git push -u origin 18.0
```

---

## PASO 7 — Crear rama 17.0

```powershell
git checkout -b 17.0
```

Abre `qweb_report_analyzer\__manifest__.py` y cambia:
```python
'version': '18.0.1.0.0',
```
por:
```python
'version': '17.0.1.0.0',
```
Guarda y vuelve a PowerShell:

```powershell
git add qweb_report_analyzer/__manifest__.py
```
```powershell
git commit -m "Branch 17.0 - initial release"
```
```powershell
git push -u origin 17.0
```

---

## PASO 8 — Verificar en GitHub

Ve a: **https://github.com/josebertorelli/qweb-report-analyzer**

Verifica que:
- ✅ Hay 3 ramas: `17.0`, `18.0`, `19.0` (las ves en el selector de ramas)
- ✅ La rama `19.0` tiene todos los archivos
- ✅ El `__manifest__.py` en cada rama tiene la versión correcta

---

## PASO 9 — Publicar en la Odoo App Store

1. Ve a **https://apps.odoo.com** e inicia sesión (o crea una cuenta gratuita)
2. Haz clic en tu avatar → **My Account** → **My Apps**
3. Busca el botón **"Submit an App"** o **"Upload"**
4. Selecciona **"GitHub repository"**
5. Autoriza el acceso a GitHub cuando te lo pida
6. Escribe la URL del repo:
   ```
   https://github.com/josebertorelli/qweb-report-analyzer
   ```
7. Odoo detectará automáticamente las ramas `17.0`, `18.0`, `19.0` y creará 3 versiones del addon
8. Completa el formulario de publicación (nombre, categoría, precio: 0)
9. Envía para revisión — Odoo tarda 1-3 días laborables en aprobar

---

## PASO 10 — Después de publicar: flujo de actualizaciones

Cada vez que quieras actualizar el addon:

```powershell
# 1. Ir a la rama que quieres actualizar
git checkout 19.0

# 2. Hacer tus cambios en los archivos

# 3. OBLIGATORIO: subir la versión en __manifest__.py
#    Ejemplo: 19.0.1.0.0 → 19.0.1.0.1

# 4. Commit y push
git add .
git commit -m "descripcion del cambio"
git push origin 19.0
```

> ⚠️ Si no subes la versión en el manifest, Odoo ignora el push y no actualiza el addon en la tienda.

Para actualizar las 3 ramas (cuando el cambio aplica a todas):
```powershell
git checkout 19.0
# editar version a 19.0.1.0.1
git add . && git commit -m "fix: descripcion" && git push origin 19.0

git checkout 18.0
# editar version a 18.0.1.0.1
git add . && git commit -m "fix: descripcion" && git push origin 18.0

git checkout 17.0
# editar version a 17.0.1.0.1
git add . && git commit -m "fix: descripcion" && git push origin 17.0
```

---

## Problemas comunes

**"remote origin already exists"**
```powershell
git remote remove origin
git remote add origin https://github.com/josebertorelli/qweb-report-analyzer.git
```

**"failed to push — repository not found"**
- Verifica que el repo existe en GitHub y que el nombre es exactamente `qweb-report-analyzer`
- Verifica que iniciaste sesión correctamente en el paso de autenticación

**"Updates were rejected because the tip of your current branch is behind"**
```powershell
git push --force-with-lease origin 19.0
```

**El push no pide autenticación y falla**
```powershell
git config --global credential.helper manager
```
Luego vuelve a intentar el push.

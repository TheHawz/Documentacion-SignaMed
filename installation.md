# Guía para desarrollar en Ubuntu

## Instalar node

versión: `12.x`

```
sudo apt update
sudo apt -y upgrade

sudo apt -y install curl dirmngr apt-transport-https lsb-release ca-certificates
curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
```


## Comprobar que **node** y **npm** están correctamente instalados
```
node -v 
npm -v
```

## Configurar una carpeta para que npm pueda instalar todo

Directamente extraido de [AQUÍ](https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally):

1. Crea el siguiente directorio para almacenar los paquetes globales de NPM:

    ```
    mkdir ~/.npm-global
    ```

2. Configura npm para usar esta carpeta:

    ```
    npm config set prefix '~/.npm-global'
    ```

3. Añade esta carpeta a la variable path para poder acceder a estos paquetes. Desde la terminal ejecuta `sudo gedit ~/.bashrc` y añade esta linea al final de todo:

    ```
    export PATH=~/.npm-global/bin:$PATH
    ```

4. Reinicia la terminal para que se actualice la variable PATH y listo.


## Instalar dependencias *globales*

- expo-cli & yarn: `npm i expo-cli yarn -g`

Si da algun error relacionado con EACCES, es que el paso anterior está mal ejecutado:

Prueba a ejecutar `$PATH` en la terminal para comprobar si la carpeta que creamos antes está en la variable PATH. 

Si no está, abre el fichero `.bashrc` para ver si la linea que añadimos en el anterior paso está ahi, etc. 


## Comprobar que git está instalado

`git -v`

Si git no está instalado: `sudo apt install git`

### Instalar github-cli (opcional)

*Extraído de [Aquí](https://github.com/cli/cli/blob/trunk/docs/install_linux.md#official-sources)*

```
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo gpg --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null

sudo apt update

sudo apt install gh
```

Comprobar la isntalación usando `gh --version`

## Pequeños detalles de configuración

Te pedirá logearte con gh y con git para poder hacer commits y clonar repos.

`gh auth login` y sigue las instrucciones en pantalla

Para poder hacer commits con git: 
```
git config --global user.name "tu nombre"
git config --global user.email nombre@correo.com
```

## Extensiones de VSCode:

- [Auto Close Tag](https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-close-tag)
- [Auto Complete Tag](https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-complete-tag)
- [Auto Rename Tag](https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-rename-tag)
- [Expo Tools](https://marketplace.visualstudio.com/items?itemName=byCedric.vscode-expo)
- [React Native Tools](https://marketplace.visualstudio.com/items?itemName=msjsdiag.vscode-react-native)
- [ES7 Snippets](https://marketplace.visualstudio.com/items?itemName=dsznajder.es7-react-js-snippets)
- [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)
- [npm Intellisense](https://marketplace.visualstudio.com/items?itemName=christian-kohler.npm-intellisense)

ESLint es un *linter*, te avisa de potenciales problemas de estilo y/o errores de sintaxis.
Te aconsejo tambien usar Prettier, para mantener el código con el mismo formato

## Descargar el proyecto y ejecutar `expo start`

```
gh repo clone speechsigns/signamed
cd SignaMed
code .
yarn
expo start
```

Por orden: *clonar la carpeta*, *moverte a ella*, *iniciar VSCode en esta carpeta*, *instalar todo usando yarn* e *iniciar el servidor de expo*.

# SignaMed

#### Índice

1. [Introducción](#introducción)
2. [Bases de JavaScript necesarias y recomendaciones de estilo](#bases-de-javascript-necesarias-y-recomendaciones-de-estilo)
   - [Definicion de variables](#definicion-de-variables)
   - [Definicion de funciones](#definicion-de-funciones)
   - [Async](#async)
   - [Nomenclatura](#nomenclatura)
   - [Typescript](#typescript)
   - [Componentes básicos de una aplicación en React Native](#componentes-básicos-de-una-aplicación-en-react-native)
   - [Manejo del estado de la aplicación](#manejo-del-estado-de-la-aplicación)
3. [Módulos de terceros usados](#módulos-de-terceros-usados)
   - [Expo](#expo)
   - [React Navigation v5](#react-navigation-v5)
   - [Firebase](#firebase)
   - [Redux](#redux)

## Introducción

Este documento recoje las decisiones de diseño a la hora de crear la primera versión de SignaMed.

## Bases de JavaScript necesarias y recomendaciones de estilo

### Definicion de variables

- `const`: Crea un objeto inmutable, se usará para funciones o tipos de datos complejos, en los que la variable es realmente un puntero; o para valores constantes.
- `let` o `var` se usaran para tipos de datos sencillos que requieran cambiar de valor.

```javascript
const a = 0
a = 1           # incorrecto
let b = 0
b = 1           # correcto
```

### Definicion de funciones

Las funciones se crear en tiempo de ejecución gracias a la instruccion necesaria.

```javascript
const getPi = () => {       # funcion sin parametros
                            # de entrada que devuelve un numero
    return 3.141592
}

function getPi() {          # Exactamente lo mismo
    return 3.141592
}

# Los siguientes ejemplos se usarán al pasar una función como parámetro
# a otra función.

() => { return 3.141592 }   # Lo mismo pero no tenemos
                            # el puntero a esta funcion
() => 3.141592              # Otra forma de escribir lo último
```

En ese caso, `getPi` sería un puntero. Este se puede usar para pasar como parámetro a otras funciones.

### Async

Una funcion asíncrona es aquella que no se sabe de antemano su tiempo de ejecución, por ejemplo, recuperar de la base de datos un valor.

A lo largo del proyecto el siguiente ejemplo se repite varias veces, por lo que queda aquí aclarado:

```javascript
getSign(id).then((sign) => {
  console.log("Navigating to Traduccion... {sign, canGoBack: true}");
  navigation.navigate("App", {
    screen: "Traducción",
    params: { sign, canGoBack: true },
  });
});
```

`getSign` es una funcion que recibe el ID único del objeto que tiene que recuperar. Esta funcion de vuelve un objeto de tipo `Promise`.

Esta promesa, tiene un método llamado `then` que recibe una función (definida como `(...) => {...}`) cuyo parámetro de entrads es el objeto al que se resuelve la promesa y ejecuta la fucionalidad deseada.

Por otro lado, `getSign` se define así:

```javascript
function getSign(signId): {
  return new Promise((resolve, reject) => {
    firebase
      .firestore()
      .collection(COLLECTION.LEX_40)
      .doc(signId)
      .get()
      .then((doc) => {
        if (doc.exists) resolve(doc2sign(doc));
      })
      .catch(reject);
  });
}
```

Las funciones `resolve` y `reject` desencadenan las fuciones que se les pasa a los métodos del objeto `Promise` `.then()` y `.catch()` correspondientemente.

### Nomenclatura

Para los nombres de las funciones se han seguido las siguientes reglas:

- Nombres de funciones y variables en `camelCase`.
- Nombres de clases e interfaces (o tipos) en `PascalCase` (en React Native las clases se definen como funciones, pero para distinguir las funciones que devuelven un elemento JSX de las que no, se usa esa primera letra mayúscula).
- Valores constantes en mayúsculas separadas por guión: `VALOR_APROX_PI = 3.14`
- Variables y setters en `camelCase`, con el mismo nombre solo que el setter comienza por `set`. Ej.: `nombre` y `setNombre`
- Los parámetros de tipo `onSomething` siempre reciben una función llamada `handleSomething`. Por ejemplo, la función que define el comportamiento de un _botón rojo_ se llamada `handleRedButtonPress` y el botón tendrá un campo llamado `onPress`. Si ese botón implementa la funcionalidad de `onLongPress`, la función correspondiente sería `handleRedButtonLongPress`.

### Typescript

Typescript es un lenguaje que se construye sobre JavaScript añadiendo definiciones de tipo estáticas. Esto asegura poder describir la forma de un objeto, proporcionando asi una forma de validad si el código funciona correctamente.

TypeScript se ha usado en la inmensa mayoría del código de SignaMed y es un objetivo futuro poder añadir estas definiciones de tipo.

Las extensiones relacionadas con TypeScript son `.ts` y `.tsx`, siendo la última aquella que se usa en los ficheros que contienen definiciones de Componentes

Esto es un ejemplo de algunos de los tipos creados para la aplicación, se encuentran en el fichero `types/index.ts`

```javascript
export interface SignMinimal {
  id: string;
  name: string;
}
export interface Sign extends SignMinimal {
  definition: string;
  tags: string[];
  related: string[];
  urls: {
    sign: string,
    definition: string,
  };
}

export interface SignSearch extends SignMinimal {
  search: string;
}
```

Typescript no solo sirve para darle forma a los objetos, sino tambien para poder comprobar que las funciones reciben los parámetros del tipo necesario, y saber de antemano el tipo del resultado.

```javascript
function add(a: number, b: number): number {
  return a + b;
}
```

Para entrar en mayor profundidad se recomienda leer la [documentación](https://www.typescriptlang.org/docs/) en la web oficial y ver este video de Ben Awad en el que explica en 20 minutos una introducción a este lenguaje: [LINK](https://www.youtube.com/watch?v=se72XMlG1Ro)

### Componentes básicos de una aplicación en React Native

Aquí se explica como se atomiza una aplicación y se definen algunos de los términos que se usaran en el resto de la documentación.

- Una **applicación** está formada por 1 o varias **pantallas** las cuales estan agrupadas en **Navegadores** (proporcionados por React Navigation v5).
- Estos navegadores a su vez pueden agruparse en otros navegadores para crear navegaciones más complejas.
- Cada pantalla está formada por **Componentes**

### Manejo del estado de la aplicación

A la hora de diseñar una aplicación con una Interfaz Gráfica (GUI) es importante la división entre estado (información) y representación.

En React Native, como hemos visto en la anterior sección, la gran división que resulta obvia es la dividir la aplicación en pantallas y estas en Componentes.

La gran mayoría del estado de la aplicación se considera _privado_, es decir, no se comparte entre pantallas ni componentes. Se podría decir que estos elementos están autocontenidos.

Pero no siempre interesa que sea así, a veces un componente necesita cambiar el estado de su _padre_. En este caso, cuando el padre instancia un componente, le puede pasar una función que sirva de _callback_ para poder cambiar, desde el hijo, el estado del padre.

Ejemplo

```javascript
# Definimos al padre, como una pantalla con un solo componente
# Este componente se encarga de modificar un valor de texto.
const Screen = () => {
    # Definimos una variable de estado y un setter
    const [nombre, setNombre] = useState('')

    # Devolvemos un elemento JSX que visualizar
    return (
        <View>
            <Input callback={setNombre}/>
        </View>
    )
}

# Definimos al hijo, este se encargara de modificar el estado del padre
# Gracias a este callback que recibe a la hora de instanciarlo.
const Input = (
    callback: React.Dispatch<React.SetStateAction<string>>
    ) => {
    # ...

    return (<></>)
}
```

Un detalle que no puede pasar desapercibido es que el setter no es una simple función que recibe un parámetro y no devuelve nada (`(value: string) => void`). Es un `Dispatch` esto es un indicativo de que el estado se comporta de manera **asíncrona**. Es decir, habrá que esperar a que el estado se actualice par poder acceder al nuevo valor. Por ello será normal encontrar esto a lo largo del proyecto:

```javascript
const Pantalla = () => {
    const [name, setName] = useState('')

    function f() {
        setName('Pablo')
    }

    # useEffect recibe una funcion (primer parámetro), a ejecutar cuando una
    # de las dependencias (el segundo parámetro) se actualice.
    useEffect(()=>{
        console.log(name) # Pablo
    }, [name])

    # ...
}
```

Más adelante veremos más en detalle las instrucciónes `useState` y `useEffect` junto al resto de _hooks_ una parte fundamental de React y React Native.

Para aquella información (de forma equivalente se puede decir _estado_) que sea

## Módulos de terceros usados

### Expo

Expo es un _framework_ y una plataforma para el desarrollo de aplicaciones para React Native. Es un conjunto de herramientas y servicios que ayuda a desarrollar, compilar y desplegar una aplicación en iOS y Android.

De expo se ha partido de su _Managed Workflow_, el cual omite cualquier tipo de código nativo para simplificar el desarrollo. Si en algún momento fuese necesario introducir código nativo, se puede hacer un `eject` en cualquier momento.

Para más información consultar los siguientes enlaces:

- [Managed vs Bare Workflows](https://docs.expo.io/introduction/managed-vs-bare/)
- [Limitaciones del Managed Workflow](https://docs.expo.io/introduction/why-not-expo/)
- [Como configurar el proyecto usando el Managed Workflow](https://docs.expo.io/workflow/configuration/)
  - [Propiedades del `app.json`](https://docs.expo.io/versions/latest/config/app/)

### React Navigation v5

Es el paquete que proporciona la funcionalidad necesaria para navegar entre pantallas.

- [Documentación](https://reactnavigation.org/)
- [Navegación entre pantallas](https://reactnavigation.org/docs/navigating/)
- [Pasar parámetros a pantallas](https://reactnavigation.org/docs/params/)
- [Agrupar navegadores](https://reactnavigation.org/docs/nesting-navigators/)

### Firebase

Para manejar la base de datos de Google (Firestore) y el módulo de _Auth_.

- [Uso](https://rnfirebase.io/firestore/usage)
- [Uso con _FlatLists_](https://rnfirebase.io/firestore/usage-with-flatlists)

### react-native-paper

Librería que proporciona el 90% de componentes básicos usados. Sigue las _Material Guidelines_ de Google para proporcionar uniformidad. Es **esencial** usar los componentes de esta librería cuando sea posible.

- [Docs](https://callstack.github.io/react-native-paper/)
- [Theming](https://callstack.github.io/react-native-paper/theming.html)
- [Integración con React Navigation](https://callstack.github.io/react-native-paper/theming-with-react-navigation.html)
- [AppBar con React Navigation](https://callstack.github.io/react-native-paper/integrate-app-bar-with-react-navigation.html)

### Redux

Para el manejo del estado (información) de la base de datos: Signos, favoritos, historial, etc.

- [¿Por qué usar Redux?](https://react-redux.js.org/introduction/why-use-react-redux)
- [](https://react-redux.js.org/introduction/getting-started)
- []()

## Conocimientos básicos de React Native para entender el código

### Hooks

#### useState

Sirve para crear variables de estado. El comportamiento del `setter` es asíncrono, eso quiere decir que el estado no se actualiza instantaneamente, tarda un poco.

```javascript
// Iniciar estado a un valor concreto. El tipo de Var es el mismo que el de initialState
const [var, setVar] = useState(initialState)

// Bool valdrá undefined en el momento de instanciación. El tipo será: undefined | boolean. Es decir, o indefinido o booleano.
// Las dos lineas siguientes son idénticas, en la segunda se definen todos los tipos de forma explicita, mientras que en la primera el undefined se infiere.
const [bool, setBool] = useState<boolean>()
const [bool, setBool] = useState<undefined | boolean>(undefined)

// Igual que el primer ejemplo, pero en este caso el tipo es complejo. JSON con 3 parámetros de tipos: entero, entero y booleano
const [complex, setComplex] = useState({par_a: 1, par_b: 2, par_c: true })
```

El setter se puede usar pasándole como parámetro un cierto valor o una función. Cuando la lógica trás actualizar un valor es constante a lo largo de distintas iteraciones, mejorará el rendimiento usar una función.

```javascript
const [time, setTime] = useState(10);

setTime(0);
// Reduce en una unidad el tiempo actual.
setTime(time - 1);
// Esta vez se le pasa al setter una función. Esta función tiene un parámetro cuyo nombre es DISTINTO al valor de la variable. Esta distinción se hizo para observar que esta función siempre se comportará como uno espera.
setTime((currentTime: number) => currentTime - 1);
```

#### useEffect

Se usa para definir comportamientos lanzados por ciertos _eventos_. Recibe 2 parámetros, una función y una lista de dependencias. Si la lista de dependencias está vacía, se ejecutará al inicio del componente, si directamente no se le pasa una lista vacía, la función se ejecutará en cada renderizado del componente.

```javascript
function f(){
  ...
}
useEffect(f, [dep1, dep2, ...])

// Exactamente lo mismo.
useEffect(()=>{}, [dep1, dep2, ...])

```

Este hook se usará en varias ocasiones con diferences motivos:

- Inicializar valores de estado (sin usar el `initialState` del estado). Por ejemplo, para recuperar valores de la base de datos.
- Lógica de actualizar ciertos componentes
  ```javascript
  // Cada vez que la variable input cambia de valor
  // Se llama a la funcion handleSearch con este nuevo valor.
  useEffect(() => {
    handleSearch(input.value);
  }, [input]);
  ```

#### useCallback

Este hook devuelve un _useEffect_ memorizado, para más información sobre qué significa esto, mirar la documentación.

La explicación rápida de porqué se debe usar es la siguiente:

Supongamos el ejemplo siguiente

```javascript
// Se inicializa un contador a 10
const [time, setTime] = useState(10);

// Se crea una función para definir el comportamiento del click
const handleClick = () => {
  setTime(time - 1);
};

// Un objeto consume esta función
return <Child onClick={handleClick} />;
```

Cada vez que `time` cambie, el _callback_ cambiará, forzando que `Child` se renderice de nuevo, innecesariamente. La forma de evitar estos renderizados podría ser: usando una función `memorizada` o cambiando el parámetro del setter

```javascript
// Se inicializa un contador a 10
const [time, setTime] = useState(10);

// Se crea una función para definir el comportamiento del click
const handleClick = useCallback(() => {
  setTime((t) => t - 1);
}, []);

// Un objeto consume esta función
return <Child onClick={handleClick} />;
```

Para una explicación más detallada: [Aquí](https://dmitripavlutin.com/dont-overuse-react-usecallback/)

#### Más info

Para más info y entendimiento se recomiendan esta serie de videos:

- [Una manera eficiente de estructurar proyectos de React Native](https://cheesecakelabs.com/blog/efficient-way-structure-react-native-projects/)
- [Common React Mistakes](https://www.youtube.com/watch?v=UQkTu-PQ5gQ)
- [React Context and Hooks](https://onderonur.netlify.app/blog/state-management-and-performance-optimizations-with-react-context-api-and-hooks/)

## Distribución del código.

Si bien el código necesitaría alguna que otra refactorización, ya que no todos los elementos siguen las directrices que se redactarán a continuación, aquí se explican las distintas carpetas en las que está organizado el proyecto y los distintos ficheros.

### Extensiones de los ficheros

- `js`: Fichero JavaScript
- `jsx`: Fichero JavaScript que define un componente.
- `ts`: Fichero TypeScript
- `tsx`: Fichero TypeScript que define un componente.

### Carpetas

- `.github`
- `src`
  - `api`: Principalmente funciones y librerías con la lógica de "_negocio_"
  - `assets`: Imágenes y otros recursos estáticos.
  - `components`: Algunos de los pequeños componentes que forman las pantallas. Aquellos componentes que se vayan a reutilizar en varias pantallas deben ir aquí.
  - `navigations`: Todos los navegadores, el principal y aquellos que están anidados a partir de él. Los nombres de las pantallas y otra información de las pantallas se cambia aquí.
  - `redux`: Aquí se guarda la información acerca de los `store` y otros elementos de Redux. Aquí se guarda y se maneja la información de la lista de Signos.
  - `scenes`: Aquí se definen todas las pantallas de la aplicación.
    - `app`
    - `login`
    - `signup`
  - `styles`: Estilos que se comparten entre pantallas y componentes.
  - `types`: Tipos necesarios para la aplicación, desde los _signos_ hasta otra información como los _bounding boxes_.

###

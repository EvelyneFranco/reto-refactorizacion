# Reflexión final

**Nombre:** Evelyne Franco<br>
**Matrícula:** N/A<br>
**Fecha:** 7 de octubre de 2026

*(10-15 líneas)*

Responde: ¿Qué tan útil fue Claude Code para detectar y corregir los problemas?
¿Qué propuso la IA que tú no habías notado? ¿En qué casos tuviste que corregir
o rechazar sus sugerencias? ¿Qué aprendiste sobre refactorizar con apoyo de IA?

La IA, en este caso Claude, me ha ayudado mucho a entender temas con los que no estoy familiarizada y a poder trabajar en ellos. También me ha ayudado en temas que sí son de mi área de trabajo, acelerando lo que hago.

Detectar los problemas y analizar el código me hubiera tomado muchísimo tiempo; con la IA tuve ese diagnóstico mucho más rápido.

En el prompt inicial fui clara: "explícalo como si fuera para un junior". La razón es que no estoy muy familiarizada con Python, siempre he trabajado con TypeScript, y era importante para mí entender qué iba a aplicar la IA y qué estaba proponiendo. Algunos puntos del reporte que le pedí generar fueron cosas nuevas para mí que, por mi poca experiencia con el lenguaje, no hubiera detectado. Por ejemplo, al reorganizar las validaciones, cambiar `cantidad > 0` por `cantidad <= 0` parece lo mismo, pero no lo es: con un valor `NaN` ("no es un número") ambas comparaciones dan falso, y una venta inválida se habría registrado. La IA lo detectó, conservó la comparación original y lo comprobó contra el código anterior; yo no lo hubiera notado.

Lo que tuve que corregir fue la configuración de Git y GitHub: la IA configuró el repositorio sin preguntarme y usó el correo de mi trabajo en un proyecto de la escuela. Al detectarlo, le pedí que primero me preguntara qué iba a implementar y que solo continuara con mi visto bueno. También cambié el orden de las refactorizaciones según lo que yo consideré más importante.

Con la IA, una refactorización que puede tomar días o meses, según el proyecto, se hace en algunas horas, y a veces de maneras que no se me hubieran ocurrido. Lo que sí considero importante mencionar es que debemos entender qué está implementando la IA: no siempre es lo correcto, a veces tenemos que corregirla y no hay que decirle que sí a todo.

---
title: "Introducción Vulnerabilidades"
---

## ¿Qué entendemos por vulnerabilidad?

La **seguridad** puede entenderse como la aplicación y ejecución de políticas por medio de mecanismos de defensa sobre datos y recursos. En esa misma línea, la **seguridad de software** se enfoca en evaluar, mejorar, hacer cumplir y comprobar propiedades de seguridad del software, con el fin de permitir su uso intencionado y evitar usos no previstos que puedan causar daño.

Dentro de ese marco, es importante distinguir entre **bug** y **vulnerabilidad**. Un *bug* es una falla en un programa o sistema que produce un resultado inesperado. Una **vulnerabilidad**, en cambio, es una debilidad del software que permite que un atacante aproveche una falla para escalar privilegios, alterar el estado del sistema, filtrar información o ejecutar acciones no autorizadas. Para que exista una vulnerabilidad explotable, deben darse al menos tres condiciones: que el sistema sea susceptible a la falla, que el adversario tenga acceso a ella y que cuente con la capacidad de explotarla.

Esta distinción es importante porque no todo error de software se transforma automáticamente en un problema de seguridad. Para que una falla pase a ser relevante desde el punto de vista defensivo, debe existir una ruta realista mediante la cual un atacante pueda convertir ese defecto en una ventaja operativa.

## ¿Por qué importa estudiar vulnerabilidades?

Estudiar vulnerabilidades importa porque la seguridad de un sistema no depende solo de sus funciones, sino también de la capacidad de resistir usos no autorizados. Defender software es difícil porque el atacante necesita encontrar una sola vía efectiva de entrada, mientras que quien defiende debe bloquear todas las rutas de ataque que sean factibles dentro de un modelo de amenazas dado.

Por eso, la identificación temprana de vulnerabilidades es una práctica central para reducir riesgo técnico y operativo. Una debilidad no detectada puede abrir la puerta a filtraciones de información, alteraciones indebidas del sistema, interrupciones de servicio o escalamiento de privilegios. Además, mientras más tarde se detecta un problema de seguridad, más costosa suele ser su corrección y mayor puede ser su impacto sobre usuarios, organizaciones y equipos de desarrollo.

## Vulnerabilidades y modelo de amenazas

El concepto de **modelo de amenazas** funciona como una herramienta para enumerar y priorizar los riesgos que comprometen la seguridad de un sistema. En términos prácticos, esto obliga a preguntarse qué activos son valiosos, qué componentes son más expuestos y cuáles son las amenazas más relevantes según el contexto de uso.

Esta idea es especialmente útil al estudiar vulnerabilidades, porque permite pasar de una noción abstracta de “falla” a una evaluación más concreta del riesgo. Una misma debilidad puede tener implicancias muy distintas dependiendo de quién puede alcanzarla, qué capacidades tiene el atacante y qué efecto produce sobre la confidencialidad, integridad o disponibilidad del sistema.

Como referencia conceptual general para estas nociones, resulta útil revisar el material **seguridad.pdf** del curso, especialmente en lo relativo a seguridad de software, modelo de amenazas y distinción entre bugs y vulnerabilidades.

## Vulnerabilidades, severidad y gestión del riesgo

No todas las vulnerabilidades tienen la misma criticidad. Su gravedad depende de factores como la facilidad de explotación, el impacto esperado, el contexto del sistema afectado y la existencia o no de medidas compensatorias. Por eso, además de detectar hallazgos, resulta necesario priorizarlos. Conceptos como severidad, riesgo y remediación son parte central del trabajo de análisis, ya que permiten distinguir entre problemas urgentes, mejoras importantes y observaciones de menor impacto inmediato.

Desde una perspectiva formativa, esto implica comprender que el análisis de vulnerabilidades no termina al producir un reporte. El valor real aparece cuando esos resultados se interpretan, se conectan con el contexto del proyecto y se transforman en decisiones concretas de corrección, seguimiento o mitigación.

## Relación con este módulo

En este módulo, el tema se aborda desde dos ángulos complementarios. Por una parte, se revisa el análisis estático de código con herramientas como [**CodeQL**](https://codeql.github.com/docs/contents/) para detectar problemas de seguridad directamente en los repositorios. Por otra, se examinan vulnerabilidades conocidas presentes en dependencias y componentes utilizados por esos proyectos con herramientas como [**Grype**](https://oss.anchore.com/docs/guides/vulnerability/getting-started/). De ese modo, el material no se limita a mostrar herramientas, sino que permite entender que una estrategia de seguridad razonable necesita observar tanto el código propio como el ecosistema de software del que depende.

Los notebooks posteriores desarrollan esa idea de manera aplicada. Algunos se enfocan en la ejecución de análisis y en la inspección de resultados; otros documentan la lógica de los scripts que automatizan esos flujos. Esta introducción, en cambio, busca entregar el marco conceptual mínimo para comprender por qué esos análisis son relevantes y qué tipo de preguntas ayudan a responder dentro de un proceso de desarrollo seguro.

## Lista de Referencias

- [CodeQL Documentation](https://codeql.github.com/docs/contents/)
- [Grype Getting Started](https://oss.anchore.com/docs/guides/vulnerability/getting-started/)

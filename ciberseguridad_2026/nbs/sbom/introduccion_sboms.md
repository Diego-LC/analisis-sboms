---
title: "Introducción SBOMs"
---

## ¿Qué es un SBOM?

Un **Software Bill of Materials (SBOM)** es un inventario estructurado de los componentes que forman parte de una aplicación o artefacto de software. En términos simples, cumple un rol similar al de una lista de ingredientes: identifica bibliotecas, paquetes, dependencias, herramientas y otros elementos utilizados durante el desarrollo, la compilación y la distribución de un sistema. Su valor no está solo en enumerar componentes, sino también en aportar contexto sobre su origen, sus versiones y la relación que mantienen entre sí.

En el desarrollo moderno, donde es habitual reutilizar paquetes de código abierto, imágenes de contenedores y dependencias de terceros, contar con esa visibilidad se ha vuelto especialmente importante. Un SBOM permite comprender mejor qué software se está utilizando realmente, qué tan amplio es el árbol de dependencias y cuáles son los puntos que podrían requerir revisión desde una perspectiva de seguridad, cumplimiento o mantenimiento.

## ¿Por qué los SBOMs han tomado tanta relevancia?

La seguridad de la cadena de suministro de software se ha convertido en una preocupación central para organizaciones públicas y privadas. Incidentes ampliamente conocidos, como ataques a proveedores de software o vulnerabilidades críticas en componentes reutilizados de manera masiva, han demostrado que no basta con revisar solo el código propio. También es necesario saber con precisión qué componentes externos forman parte de una solución y cómo impactan en su nivel de riesgo.

En ese contexto, los SBOMs aportan una base concreta para mejorar la trazabilidad y la transparencia. Permiten identificar dependencias potencialmente vulnerables, revisar si existen licencias incompatibles con políticas internas y fortalecer la capacidad de respuesta ante nuevos hallazgos de seguridad. Además, su adopción ha ido creciendo no solo por razones técnicas, sino también por exigencias regulatorias y por una demanda cada vez mayor de evidencia sobre el origen y la composición del software.

## Estándares y automatización

Para que un SBOM sea realmente útil, su generación e interpretación deben poder automatizarse. Por eso existen estándares de intercambio que facilitan producir, compartir y procesar esta información de manera consistente. Entre los formatos más conocidos se encuentran [**CycloneDX**](https://cyclonedx.org/specification/overview), actualmente desarrollado como estándar abierto para transparencia de la cadena de suministro, y [**SPDX**](https://spdx.dev/use/specifications/), estándar internacional abierto utilizado ampliamente para describir componentes, licencias y relaciones entre artefactos de software. Ambos son ampliamente utilizados en prácticas de seguridad y cumplimiento.

La automatización es clave porque un SBOM pierde valor si se genera una sola vez y luego queda desactualizado. En entornos de desarrollo continuos, donde cambian dependencias, versiones y artefactos con frecuencia, lo recomendable es integrar la generación de SBOMs al flujo de trabajo habitual. De esa forma, el inventario puede mantenerse vigente y complementarse con procesos de análisis de vulnerabilidades y revisión de licencias.

Como referencia institucional más general sobre el tema, también resulta útil revisar los materiales de [**CISA sobre SBOM**](https://www.cisa.gov/sbom) y los recursos de [**NTIA sobre Software Bill of Materials**](https://www.ntia.gov/page/software-bill-materials), ya que ambos reúnen lineamientos, definiciones y documentos introductorios ampliamente utilizados en la conversación pública sobre transparencia de componentes de software.

## Contenido del Módulo

En este módulo, los materiales siguientes aterrizan esta idea general en un contexto práctico. Por una parte, se muestra cómo generar SBOMs para un conjunto de repositorios y cómo aprovechar esos resultados para obtener una visión consolidada de los componentes detectados. Por otra, se presenta la lógica general del script que automatiza ese proceso, de modo que resulte claro cómo llevar esta práctica desde una explicación conceptual a una ejecución reproducible.

Así, esta introducción busca responder el **por qué** de los SBOMs, mientras que los notebooks posteriores desarrollan el **cómo** incorporarlos a un flujo de trabajo real. La combinación de ambas perspectivas es relevante: no se trata solo de producir archivos con dependencias, sino de entender por qué esos datos son útiles para la gestión de riesgos, la observabilidad del software y la seguridad de la cadena de suministro.

## Lista de Referencias

- [CycloneDX Specification Overview](https://cyclonedx.org/specification/overview)
- [SPDX Specifications](https://spdx.dev/use/specifications/)
- [CISA: Software Bill of Materials (SBOM)](https://www.cisa.gov/sbom)
- [NTIA: Software Bill of Materials](https://www.ntia.gov/page/software-bill-materials)

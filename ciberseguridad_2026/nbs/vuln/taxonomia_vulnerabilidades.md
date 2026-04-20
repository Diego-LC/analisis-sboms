---
title: "CVE, CWE, CVSS, NVD y MITRE ATT&CK"
---

## ¿Por qué conviene distinguir estos conceptos?

Cuando se estudian vulnerabilidades, es habitual encontrarse con siglas que parecen referirse a lo mismo, pero que en realidad cumplen funciones distintas. Distinguir entre **CWE**, **CVE**, **CVSS**, **NVD** y [**MITRE ATT&CK**](https://attack.mitre.org/) ayuda a interpretar mejor reportes técnicos, priorizar hallazgos y comunicar riesgos con mayor precisión.

En términos generales, estas nociones responden preguntas diferentes:

- **CWE**: ¿qué tipo de debilidad o error está presente?
- **CVE**: ¿qué vulnerabilidad pública y específica fue identificada?
- **CVSS**: ¿qué tan severa parece esa vulnerabilidad?
- **NVD**: ¿dónde se consolida información técnica y de priorización sobre CVEs?
- **ATT&CK**: ¿cómo podría actuar un adversario una vez que explota o aprovecha ciertas condiciones del sistema?

## CWE: categorías de debilidades

Un [**CWE**](https://www.cvedetails.com/cwe-definitions/) describe una **debilidad común** que puede dar origen a vulnerabilidades. No apunta, en principio, a un producto ni a un incidente puntual, sino a un patrón de error o deficiencia. Por eso resulta especialmente útil en etapas de diseño, programación, revisión y enseñanza, ya que permite hablar de causas recurrentes y no solo de casos concretos.

Desde esta perspectiva, un CWE ayuda a responder cuál es la naturaleza del problema: por ejemplo, exposición de información, validación insuficiente, errores de autorización o manejo inseguro de entradas. En la práctica, esto vuelve a CWE muy útil para procesos de desarrollo seguro, capacitación y remediación estructural.

## CVE: vulnerabilidades específicas y públicas

Un [**CVE**](https://www.cve.org/) identifica una **vulnerabilidad concreta**, pública y distinguible en un producto, biblioteca, versión o sistema determinado. A diferencia de un CWE, que es una clase de debilidad, un CVE apunta a una instancia específica que puede ser rastreada y discutida de forma estandarizada.

Esto permite que fabricantes, equipos de seguridad, analistas y herramientas hablen del mismo problema usando un identificador común. En otras palabras, el CVE funciona como una referencia compartida para coordinar análisis, priorización, mitigación y seguimiento.

## CVSS: severidad y priorización

El [**CVSS**](https://www.first.org/cvss/specification-document) es un sistema de puntaje que busca estimar la **severidad** de una vulnerabilidad. No describe la debilidad de fondo ni reemplaza el análisis contextual, pero entrega una base cuantitativa para priorizar. En términos generales, resume qué tan serio podría ser un problema considerando variables como impacto y facilidad de explotación.

Por eso, CVSS es útil para ordenar trabajo y comparar hallazgos, aunque no debería interpretarse de manera aislada. Un puntaje alto no siempre implica el mismo nivel de riesgo en todos los entornos, y uno moderado puede resultar crítico si afecta un activo especialmente sensible.

## NVD: consolidación de información sobre vulnerabilidades

La [**National Vulnerability Database (NVD)**](https://nvd.nist.gov/) opera como una base de datos que reúne y enriquece información asociada a vulnerabilidades públicas. En la práctica, es uno de los lugares más importantes para consultar detalles adicionales sobre un CVE, incluyendo puntajes, referencias y metadatos útiles para priorización técnica.

Visto de forma simple, si el CVE entrega la identidad de una vulnerabilidad, la NVD aporta una capa adicional de contexto para su análisis y gestión. Esto la vuelve particularmente relevante para herramientas automatizadas y flujos de respuesta que necesitan centralizar información pública sobre fallas conocidas.

## ¿Dónde entra MITRE ATT&CK?

[**MITRE ATT&CK**](https://attack.mitre.org/) no es un catálogo de vulnerabilidades, sino una base de conocimiento sobre **tácticas y técnicas de adversarios** observadas en escenarios reales. Su utilidad no está en decir qué debilidad existe en un sistema, sino en ayudar a describir cómo un atacante podría moverse, persistir, extraer credenciales o desplegar carga maliciosa.

Por eso, ATT&CK complementa muy bien a CWE, CVE, CVSS y NVD. Mientras esas estructuras ayudan a identificar, clasificar y priorizar vulnerabilidades, ATT&CK ayuda a contextualizar el **comportamiento adversario** que podría aparecer antes, durante o después de una explotación.

## Cómo se relacionan entre sí

Una manera práctica de entender la relación entre estos conceptos es pensar el flujo de la siguiente forma:

- Un sistema puede contener una **debilidad** clasificada como `CWE`.
- Esa debilidad puede materializarse en una **vulnerabilidad concreta** registrada como `CVE`.
- Esa vulnerabilidad puede tener una **severidad estimada** mediante `CVSS`.
- La información pública ampliada sobre ese caso puede consultarse en `NVD`.
- Si un atacante aprovecha esa condición, el comportamiento observado puede describirse con técnicas de `MITRE ATT&CK`.

Este encadenamiento ayuda a pasar desde una visión puramente técnica del defecto a una comprensión más amplia del riesgo, la priorización y el posible comportamiento ofensivo asociado.

## Relación con este módulo

En este módulo, estas distinciones son especialmente útiles para leer mejor los resultados producidos por herramientas de análisis. Por ejemplo, cuando se inspeccionan vulnerabilidades conocidas en dependencias, suele aparecer el lenguaje de `CVE`, `CVSS` y catálogos públicos. A su vez, cuando se revisan problemas de seguridad desde el código o desde patrones de implementación, resulta más natural pensar en términos de `CWE` y de causas subyacentes.

ATT&CK agrega una capa adicional de valor pedagógico, porque permite conectar hallazgos técnicos con conductas adversarias más amplias. Así, el análisis no se queda solo en “qué falla existe”, sino que también ayuda a pensar “qué podría intentar hacer un atacante con esa condición”.

## Lista de Referencias

- [CVE Program](https://www.cve.org/)
- [CVSS Specification Document](https://www.first.org/cvss/specification-document)
- [National Vulnerability Database (NVD)](https://nvd.nist.gov/)
- [Understanding the Differences Between CVE, CWE, and NVD](https://medium.com/@King_Night/understanding-the-differences-between-cve-cwe-and-nvd-e2db34633da8)
- [CWE Vs. CVE Vs. CVSS: What Are the Differences?](https://attaxion.com/blog/cwe-vs-cve-cvss-difference/)
- [CWE Definitions - CVE Details](https://www.cvedetails.com/cwe-definitions/)
- [MITRE ATT&CK](https://attack.mitre.org/)

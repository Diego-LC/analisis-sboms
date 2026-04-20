---
title: "Caso de Estudio: LiteLLM y Cadena de Suministro"
---

## ¿Por qué este caso es valioso?

El compromiso de `LiteLLM` en PyPI es un caso especialmente útil para estudiar vulnerabilidades y seguridad de la cadena de suministro porque muestra cómo un incidente no siempre comienza con una falla clásica en el código de una aplicación. En este caso, el problema relevante estuvo en la **confianza depositada en la cadena de publicación y en herramientas del ecosistema de desarrollo**, lo que permitió distribuir versiones maliciosas de un paquete legítimo.

Desde una perspectiva formativa, este caso ayuda a entender que la seguridad del software no depende solo de revisar bibliotecas vulnerables, sino también de proteger procesos de integración continua, credenciales de publicación, mecanismos automáticos de instalación y herramientas que operan con amplios permisos sobre entornos de desarrollo o despliegue.

## Resumen general del incidente

Diversos análisis públicos reportaron que el 24 de marzo de 2026 se publicaron en PyPI dos versiones maliciosas de `litellm`, `1.82.7` y `1.82.8`. La publicación no correspondía a un paquete falso o imitador, sino a versiones comprometidas del proyecto real, lo que convierte este incidente en un ejemplo claro de **ataque a la cadena de suministro**.

Los reportes coinciden en que el caso se relaciona con una campaña más amplia atribuida al actor `TeamPCP`, que ya había comprometido otras piezas del ecosistema, incluyendo herramientas y componentes asociados a flujos de CI/CD. Esto vuelve al caso particularmente interesante, porque muestra cómo el acceso robado en una etapa puede reutilizarse para comprometer proyectos distintos en pocos días.

## ¿Qué hacía el paquete malicioso?

Las fuentes consultadas describen que las versiones afectadas incorporaban mecanismos de ejecución maliciosa con dos variantes principales. En una de ellas, el código se activaba cuando la aplicación utilizaba partes específicas del paquete. En la otra, más riesgosa, el paquete incluía un archivo `.pth` que permitía ejecutar código automáticamente al iniciar el intérprete de Python.

Ese detalle es especialmente relevante, porque transforma la instalación del paquete en un evento de alto impacto: no era necesario esperar a que una funcionalidad compleja fuese invocada si el mecanismo de inicialización ya habilitaba la ejecución del payload.

## Impacto observado

Los análisis públicos describen capacidades de recolección de credenciales, exfiltración de datos, mecanismos de persistencia y actividad orientada a contenedores o entornos Kubernetes. En términos prácticos, esto implica que el impacto potencial iba mucho más allá de una simple modificación del paquete: cualquier entorno que hubiese instalado las versiones comprometidas debía tratarse como potencialmente expuesto.

Por eso, este caso también enseña una lección importante de respuesta a incidentes: cuando un paquete de uso real aparece comprometido en la cadena de suministro, el problema no se resuelve únicamente con “actualizar de versión”. En muchos casos, corresponde investigar persistencia, rotar credenciales, revisar actividad de red y analizar qué información pudo haber quedado expuesta.

## Relación con MITRE ATT&CK

Este caso conversa muy bien con [**MITRE ATT&CK**](https://attack.mitre.org/), porque varias de las conductas descritas en los análisis públicos pueden mapearse a técnicas conocidas. Entre ellas destacan:

- [**T1546.018 - Python Startup Hooks**](https://attack.mitre.org/techniques/T1546/018/), por el uso de archivos `.pth` para ejecutar código al iniciar Python.
- [**T1003 - OS Credential Dumping**](https://attack.mitre.org/techniques/T1003/), por la recolección de material sensible y credenciales en el sistema.
- [**T1610 - Deploy Container**](https://attack.mitre.org/techniques/T1610/), por la relación del caso con actividad orientada a despliegue y abuso de contenedores en entornos Kubernetes.

Este tipo de mapeo no reemplaza el análisis del incidente, pero sí ayuda a conectarlo con una taxonomía de comportamiento adversario ampliamente utilizada en investigación, detección y threat hunting.

## Lecciones para el módulo

Este caso de estudio aporta varias lecciones útiles para la sección de vulnerabilidades. Primero, muestra que no todas las amenazas relevantes aparecen como una vulnerabilidad clásica con una remediación trivial. Segundo, evidencia que herramientas de seguridad, automatización y despliegue también forman parte de la superficie de riesgo. Tercero, recuerda que los entornos con secretos, credenciales de nube y acceso a clústeres son especialmente atractivos para actores que buscan maximizar impacto.

Para el trabajo del módulo, esto ayuda a complementar el uso de herramientas como `CodeQL` y `Grype`. El análisis de código y de dependencias sigue siendo importante, pero debe convivir con una mirada más amplia sobre integridad del pipeline, publicación de paquetes, monitoreo de comportamientos anómalos y respuesta a incidentes de cadena de suministro.

## Lista de Referencias

- [How a Poisoned Security Scanner Became the Key to Backdooring LiteLLM](https://snyk.io/blog/poisoned-security-scanner-backdooring-litellm/)
- [Compromised litellm PyPI Package Delivers Multi-Stage Credential Stealer](https://www.sonatype.com/blog/compromised-litellm-pypi-package-delivers-multi-stage-credential-stealer)
- [LiteLLM and Telnyx compromised on PyPI: Tracing the TeamPCP supply chain campaign](https://securitylabs.datadoghq.com/articles/litellm-compromised-pypi-teampcp-supply-chain-campaign/)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [Event Triggered Execution: Python Startup Hooks (T1546.018)](https://attack.mitre.org/techniques/T1546/018/)
- [OS Credential Dumping (T1003)](https://attack.mitre.org/techniques/T1003/)
- [Deploy Container (T1610)](https://attack.mitre.org/techniques/T1610/)

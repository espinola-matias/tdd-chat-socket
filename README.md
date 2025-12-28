# 💬 Python TDD Chat Server

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Testing-yellow?style=for-the-badge&logo=pytest&logoColor=black)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)
![Coverage](https://img.shields.io/badge/Coverage-80%25%2B-brightgreen?style=for-the-badge)

Un servidor de chat TCP concurrente y robusto, construido desde cero con Python. Este proyecto fue desarrollado utilizando la metodología **TDD (Test Driven Development)** para garantizar la estabilidad, el manejo de errores y una arquitectura limpia.

---

## 🚀 Características Principales

* **🔌 Conexiones Múltiples:** Soporte para múltiples clientes simultáneos usando `Threading` y `Sockets`.
* **🛡️ Thread-Safe:** Implementación de `Locks` (mutex) para evitar condiciones de carrera en la gestión de clientes.
* **🧪 TDD First:** Cada funcionalidad crítica fue escrita primero como prueba unitaria antes de implementar el código.
* **📡 Difusión (Broadcast):** Los mensajes se reenvían en tiempo real a todos los usuarios conectados.
* **🛑 Manejo de Errores:** Sistema resiliente ante desconexiones abruptas de clientes sin afectar al servidor.
* **✅ Validación:** Filtros estrictos para evitar mensajes vacíos o excesivamente largos.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3
* **Redes:** Socket (TCP/IP)
* **Concurrencia:** Threading Library
* **Testing:** Pytest & Pytest-Cov

---
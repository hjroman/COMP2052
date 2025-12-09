"""
Script para iniciar todos los microservicios del sistema de biblioteca
Versión optimizada para Windows
"""

import subprocess
import time
import sys
import os

def start_service(name, path, port):
    """Inicia un microservicio en un proceso separado"""
    print(f"🚀 Iniciando {name} en puerto {port}...")
    
    # Verificar que el archivo existe
    if not os.path.exists(path):
        print(f"❌ ERROR: No se encontró {path}")
        return None
    
    # En Windows, usar CREATE_NEW_CONSOLE para cada proceso
    if sys.platform == 'win32':
        process = subprocess.Popen(
            [sys.executable, path],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    else:
        process = subprocess.Popen(
            [sys.executable, path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    
    time.sleep(3)  # Dar más tiempo para que inicie
    return process

def main():
    print("=" * 70)
    print("🏗️  INICIANDO ARQUITECTURA DE MICROSERVICIOS")
    print("=" * 70)
    print()
    print(f"📂 Directorio: {os.getcwd()}")
    print()
    
    processes = []
    
    try:
        # Servicios a iniciar
        services = [
            ("Auth Service", "services/auth_service/app.py", 5001),
            ("Books Service", "services/books_service/app.py", 5002),
            ("Members Service", "services/members_service/app.py", 5003),
            ("Loans Service", "services/loans_service/app.py", 5004),
        ]
        
        # Iniciar microservicios
        for name, path, port in services:
            process = start_service(name, path, port)
            if process:
                processes.append((name, process))
                print(f"✅ {name} iniciado (ventana separada)")
        
        print()
        time.sleep(2)
        
        # Iniciar Gateway
        gateway_path = "gateway/app.py"
        print("🌐 Iniciando API Gateway en puerto 5000...")
        gateway_process = start_service("API Gateway", gateway_path, 5000)
        
        if gateway_process:
            processes.append(("API Gateway", gateway_process))
            print("✅ API Gateway iniciado (ventana separada)")
        
        print()
        print("=" * 70)
        print("✅ TODOS LOS SERVICIOS INICIADOS")
        print("=" * 70)
        print()
        print("🌐 Accede a: http://localhost:5000")
        print()
        print("📊 Servicios activos en ventanas separadas:")
        print("   • Auth Service:    Puerto 5001")
        print("   • Books Service:   Puerto 5002")
        print("   • Members Service: Puerto 5003")
        print("   • Loans Service:   Puerto 5004")
        print("   • API Gateway:     Puerto 5000")
        print()
        print("⚠️  IMPORTANTE:")
        print("   - Se abrieron 5 ventanas (una por servicio)")
        print("   - Para detener TODO: Cierra TODAS las ventanas")
        print("   - O presiona Ctrl+C aquí y luego cierra las ventanas")
        print()
        print("=" * 70)
        
        # Mantener el script corriendo
        print("\nPresiona Ctrl+C para terminar este script...")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Script terminado")
        print("⚠️  RECUERDA: Cierra manualmente las ventanas de los servicios")
        sys.exit(0)

if __name__ == "__main__":
    main()
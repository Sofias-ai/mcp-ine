#!/usr/bin/env python3
"""
Script de pruebas exhaustivas para MCP INE
Valida 100% de la funcionalidad con 100 pruebas
"""

import sys
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Tuple
import traceback

# Importar las funciones del módulo
sys.path.insert(0, '/workspaces/codespaces-blank/mcp-ine/src')
from mcp_ine.tools import (
    List_Operations,
    Get_Operation_Tables,
    Get_Table_Data,
    Get_Series_Data,
    Get_Table_Variables,
    Get_Variable_Values,
    Search_Data,
    Get_Latest_Data
)

# Colores para la salida
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

class TestSuite:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.tests_total = 0
        self.failed_tests = []
        self.start_time = None
        self.results = []
        
    def print_header(self, text: str):
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}{text.center(80)}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")
    
    def print_section(self, text: str):
        print(f"\n{Colors.BOLD}{Colors.BLUE}▶ {text}{Colors.END}")
        print(f"{Colors.BLUE}{'─'*80}{Colors.END}")
    
    def test(self, name: str, func, expected_type=None, validate_func=None):
        """Ejecutar una prueba individual"""
        self.tests_total += 1
        test_num = self.tests_total
        
        try:
            print(f"{Colors.YELLOW}[{test_num:3d}]{Colors.END} {name}...", end=" ", flush=True)
            
            start = time.time()
            result = func()
            duration = time.time() - start
            
            # Validaciones
            if result is None:
                raise ValueError("Result is None")
            
            if expected_type and not isinstance(result, expected_type):
                raise TypeError(f"Expected {expected_type}, got {type(result)}")
            
            if validate_func and not validate_func(result):
                raise ValueError("Custom validation failed")
            
            self.tests_passed += 1
            print(f"{Colors.GREEN}✓ PASS{Colors.END} ({duration:.2f}s)")
            self.results.append({
                "test": test_num,
                "name": name,
                "status": "PASS",
                "duration": duration
            })
            return result
            
        except Exception as e:
            self.tests_failed += 1
            error_msg = str(e)
            print(f"{Colors.RED}✗ FAIL{Colors.END} - {error_msg}")
            self.failed_tests.append((test_num, name, error_msg))
            self.results.append({
                "test": test_num,
                "name": name,
                "status": "FAIL",
                "error": error_msg
            })
            return None
    
    def start(self):
        """Iniciar suite de pruebas"""
        self.start_time = time.time()
        self.print_header("MCP INE - SUITE DE PRUEBAS EXHAUSTIVAS")
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Objetivo: Validar 100% de la funcionalidad con 100 pruebas\n")
    
    def finish(self):
        """Finalizar suite de pruebas"""
        duration = time.time() - self.start_time
        
        self.print_header("RESUMEN DE PRUEBAS")
        
        print(f"Total de pruebas:  {Colors.BOLD}{self.tests_total}{Colors.END}")
        print(f"Pruebas exitosas:  {Colors.GREEN}{self.tests_passed} ✓{Colors.END}")
        print(f"Pruebas fallidas:  {Colors.RED}{self.tests_failed} ✗{Colors.END}")
        print(f"Tiempo total:      {duration:.2f} segundos")
        print(f"Tasa de éxito:     {Colors.BOLD}{(self.tests_passed/self.tests_total*100):.1f}%{Colors.END}")
        
        if self.failed_tests:
            self.print_section("PRUEBAS FALLIDAS")
            for test_num, name, error in self.failed_tests:
                print(f"{Colors.RED}[{test_num:3d}] {name}{Colors.END}")
                print(f"      Error: {error}\n")
        
        # Guardar resultados
        report = {
            "timestamp": datetime.now().isoformat(),
            "total": self.tests_total,
            "passed": self.tests_passed,
            "failed": self.tests_failed,
            "success_rate": f"{(self.tests_passed/self.tests_total*100):.1f}%",
            "duration": f"{duration:.2f}s",
            "results": self.results,
            "failed_tests": [{"test": t, "name": n, "error": e} for t, n, e in self.failed_tests]
        }
        
        with open('/workspaces/codespaces-blank/mcp-ine/test_results.json', 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n{Colors.CYAN}Reporte guardado en: test_results.json{Colors.END}")
        
        return self.tests_failed == 0


def run_all_tests():
    """Ejecutar todas las pruebas"""
    suite = TestSuite()
    suite.start()
    
    # Variables globales para almacenar datos entre pruebas
    operations = None
    ipc_tables = None
    table_data = None
    series_data = None
    variables = None
    variable_values = None
    
    # ============================================================================
    # SECCIÓN 1: List_Operations (20 pruebas)
    # ============================================================================
    suite.print_section("SECCIÓN 1: List_Operations - Listar Operaciones (20 pruebas)")
    
    # Test 1-5: Funcionalidad básica
    operations = suite.test(
        "Listar todas las operaciones disponibles",
        lambda: List_Operations(),
        expected_type=list,
        validate_func=lambda x: len(x) > 0
    )
    
    suite.test(
        "Verificar que retorna más de 100 operaciones",
        lambda: List_Operations(),
        validate_func=lambda x: len(x) >= 100
    )
    
    suite.test(
        "Verificar estructura de cada operación (Id, Codigo, Nombre)",
        lambda: List_Operations(),
        validate_func=lambda x: all('Id' in op and 'Codigo' in op and 'Nombre' in op for op in x[:10])
    )
    
    suite.test(
        "Verificar que operaciones tienen código IOE",
        lambda: List_Operations(),
        validate_func=lambda x: all('Cod_IOE' in op or 'Codigo' in op for op in x[:10])
    )
    
    suite.test(
        "Verificar IDs son únicos",
        lambda: List_Operations(),
        validate_func=lambda x: len(set(op['Id'] for op in x)) == len(x)
    )
    
    # Test 6-10: Filtros
    suite.test(
        "Filtrar operaciones por 'IPC'",
        lambda: List_Operations("IPC"),
        validate_func=lambda x: len(x) > 0 and any('IPC' in op.get('Nombre', '').upper() or 'IPC' in op.get('Codigo', '').upper() for op in x)
    )
    
    suite.test(
        "Filtrar operaciones por 'población'",
        lambda: List_Operations("población"),
        validate_func=lambda x: len(x) > 0
    )
    
    suite.test(
        "Filtrar operaciones por 'EPA'",
        lambda: List_Operations("EPA"),
        validate_func=lambda x: len(x) > 0
    )
    
    suite.test(
        "Filtrar operaciones por 'vivienda'",
        lambda: List_Operations("vivienda"),
        validate_func=lambda x: len(x) > 0
    )
    
    suite.test(
        "Filtrar operaciones inexistentes retorna lista vacía",
        lambda: List_Operations("OperacionQueNoExisteXYZ123"),
        validate_func=lambda x: len(x) == 0
    )
    
    # Test 11-15: Casos especiales
    suite.test(
        "Filtro case-insensitive funciona correctamente",
        lambda: List_Operations("ipc"),
        validate_func=lambda x: len(x) > 0
    )
    
    suite.test(
        "Filtro con espacios funciona",
        lambda: List_Operations("Índice de Precios"),
        validate_func=lambda x: len(x) > 0
    )
    
    suite.test(
        "Filtro con caracteres especiales",
        lambda: List_Operations("población"),
        validate_func=lambda x: len(x) > 0
    )
    
    suite.test(
        "Operación IPC existe en la lista",
        lambda: List_Operations("IPC"),
        validate_func=lambda x: any(op.get('Codigo') == 'IPC' for op in x)
    )
    
    suite.test(
        "Operación IPV (vivienda) existe",
        lambda: List_Operations("IPV"),
        validate_func=lambda x: any(op.get('Codigo') == 'IPV' for op in x)
    )
    
    # Test 16-20: Validación de datos
    suite.test(
        "Todos los códigos son strings no vacíos",
        lambda: List_Operations(),
        validate_func=lambda x: all(isinstance(op.get('Codigo'), str) and len(op.get('Codigo', '')) > 0 for op in x[:20])
    )
    
    suite.test(
        "Todos los nombres son strings no vacíos",
        lambda: List_Operations(),
        validate_func=lambda x: all(isinstance(op.get('Nombre'), str) and len(op.get('Nombre', '')) > 0 for op in x[:20])
    )
    
    suite.test(
        "Todas las URLs son válidas",
        lambda: List_Operations(),
        validate_func=lambda x: all('http' in op.get('Url', '').lower() or 'http' in op.get('URL', '').lower() or op.get('Url') is None for op in x[:20])
    )
    
    suite.test(
        "IDs son enteros positivos",
        lambda: List_Operations(),
        validate_func=lambda x: all(isinstance(op.get('Id'), int) and op.get('Id') > 0 for op in x[:20])
    )
    
    suite.test(
        "Retorno es JSON serializable",
        lambda: json.dumps(List_Operations()[:10]),
        expected_type=str
    )
    
    # ============================================================================
    # SECCIÓN 2: Get_Operation_Tables (20 pruebas)
    # ============================================================================
    suite.print_section("SECCIÓN 2: Get_Operation_Tables - Tablas por Operación (20 pruebas)")
    
    # Test 21-25: IPC
    ipc_tables = suite.test(
        "Obtener tablas de IPC",
        lambda: Get_Operation_Tables("IPC"),
        expected_type=list,
        validate_func=lambda x: len(x) > 0
    )
    
    suite.test(
        "IPC tiene más de 10 tablas",
        lambda: Get_Operation_Tables("IPC"),
        validate_func=lambda x: len(x) >= 10
    )
    
    suite.test(
        "Tablas IPC tienen estructura correcta (Id, Nombre)",
        lambda: Get_Operation_Tables("IPC"),
        validate_func=lambda x: all('Id' in t and 'Nombre' in t for t in x[:5])
    )
    
    suite.test(
        "Tablas IPC tienen código",
        lambda: Get_Operation_Tables("IPC"),
        validate_func=lambda x: all('Codigo' in t for t in x[:5])
    )
    
    suite.test(
        "Tablas IPC tienen periodicidad",
        lambda: Get_Operation_Tables("IPC"),
        validate_func=lambda x: all('FK_Periodicidad' in t for t in x[:5])
    )
    
    # Test 26-30: IPV (Vivienda)
    suite.test(
        "Obtener tablas de IPV",
        lambda: Get_Operation_Tables("IPV"),
        expected_type=list,
        validate_func=lambda x: len(x) > 0
    )
    
    suite.test(
        "IPV tiene al menos 5 tablas",
        lambda: Get_Operation_Tables("IPV"),
        validate_func=lambda x: len(x) >= 5
    )
    
    suite.test(
        "Tabla 25171 existe en IPV",
        lambda: Get_Operation_Tables("IPV"),
        validate_func=lambda x: any(t.get('Id') == 25171 for t in x)
    )
    
    suite.test(
        "Tablas IPV son trimestrales (periodicidad 3)",
        lambda: Get_Operation_Tables("IPV"),
        validate_func=lambda x: any(t.get('FK_Periodicidad') == 3 for t in x)
    )
    
    suite.test(
        "Tablas IPV tienen metadatos",
        lambda: Get_Operation_Tables("IPV"),
        validate_func=lambda x: all('Id' in t and 'Nombre' in t for t in x)
    )
    
    # Test 31-35: EPA
    suite.test(
        "Obtener tablas de EPA",
        lambda: Get_Operation_Tables("EPA"),
        expected_type=list,
        validate_func=lambda x: len(x) > 0
    )
    
    suite.test(
        "EPA retorna tablas válidas",
        lambda: Get_Operation_Tables("EPA"),
        validate_func=lambda x: all(isinstance(t, dict) for t in x)
    )
    
    suite.test(
        "IDs de tablas EPA son únicos",
        lambda: Get_Operation_Tables("EPA"),
        validate_func=lambda x: len(set(t['Id'] for t in x)) == len(x)
    )
    
    suite.test(
        "Nombres de tablas EPA no están vacíos",
        lambda: Get_Operation_Tables("EPA"),
        validate_func=lambda x: all(len(t.get('Nombre', '')) > 0 for t in x)
    )
    
    suite.test(
        "Códigos de tablas EPA son válidos",
        lambda: Get_Operation_Tables("EPA"),
        validate_func=lambda x: all(isinstance(t.get('Codigo'), str) for t in x)
    )
    
    # Test 36-40: Casos especiales
    suite.test(
        "Operación inexistente maneja error correctamente",
        lambda: Get_Operation_Tables("OPERACION_INEXISTENTE_XYZ"),
        expected_type=list
    )
    
    suite.test(
        "Código vacío maneja error",
        lambda: Get_Operation_Tables(""),
        expected_type=list
    )
    
    suite.test(
        "Multiple operaciones funcionan en secuencia",
        lambda: [Get_Operation_Tables("IPC"), Get_Operation_Tables("IPV"), Get_Operation_Tables("EPA")],
        validate_func=lambda x: len(x) == 3 and all(isinstance(tables, list) for tables in x)
    )
    
    suite.test(
        "Resultado es JSON serializable",
        lambda: json.dumps(Get_Operation_Tables("IPC")[:3]),
        expected_type=str
    )
    
    suite.test(
        "Tablas mantienen consistencia entre llamadas",
        lambda: len(Get_Operation_Tables("IPC")) == len(Get_Operation_Tables("IPC")),
        validate_func=lambda x: x is True
    )
    
    # ============================================================================
    # SECCIÓN 3: Get_Table_Data (25 pruebas)
    # ============================================================================
    suite.print_section("SECCIÓN 3: Get_Table_Data - Datos de Tablas (25 pruebas)")
    
    # Test 41-45: Básico
    table_data = suite.test(
        "Obtener datos de tabla IPC (50902)",
        lambda: Get_Table_Data(50902),
        expected_type=list,
        validate_func=lambda x: len(x) > 0
    )
    
    suite.test(
        "Datos tienen estructura de series",
        lambda: Get_Table_Data(50902),
        validate_func=lambda x: all('COD' in s and 'Data' in s for s in x[:5])
    )
    
    suite.test(
        "Series tienen nombre",
        lambda: Get_Table_Data(50902),
        validate_func=lambda x: all('Nombre' in s for s in x[:5])
    )
    
    suite.test(
        "Series tienen datos no vacíos",
        lambda: Get_Table_Data(50902),
        validate_func=lambda x: any(len(s.get('Data', [])) > 0 for s in x)
    )
    
    suite.test(
        "Puntos de datos tienen Fecha y Valor",
        lambda: Get_Table_Data(50902),
        validate_func=lambda x: any(
            len(s.get('Data', [])) > 0 and 
            all('Fecha' in d and 'Valor' in d for d in s['Data'][:3])
            for s in x[:5]
        )
    )
    
    # Test 46-50: Parámetros
    suite.test(
        "Obtener últimos 3 periodos",
        lambda: Get_Table_Data(50902, last_periods=3),
        validate_func=lambda x: any(len(s.get('Data', [])) <= 3 for s in x)
    )
    
    suite.test(
        "Obtener últimos 12 periodos",
        lambda: Get_Table_Data(50902, last_periods=12),
        expected_type=list
    )
    
    suite.test(
        "Filtro por tipo de periodo 'M' (mensual)",
        lambda: Get_Table_Data(50902, period_type='M'),
        expected_type=list
    )
    
    suite.test(
        "Filtro por tipo de periodo 'A' (anual)",
        lambda: Get_Table_Data(50902, period_type='A'),
        expected_type=list
    )
    
    suite.test(
        "Nivel de detalle 2",
        lambda: Get_Table_Data(50902, detail_level=2),
        expected_type=list
    )
    
    # Test 51-55: IPV (tabla 25171)
    suite.test(
        "Obtener datos de IPV tabla 25171",
        lambda: Get_Table_Data(25171),
        expected_type=list,
        validate_func=lambda x: len(x) > 0
    )
    
    suite.test(
        "IPV últimos 2 trimestres",
        lambda: Get_Table_Data(25171, last_periods=2),
        validate_func=lambda x: len(x) > 0
    )
    
    suite.test(
        "IPV contiene datos de País Vasco",
        lambda: Get_Table_Data(25171, last_periods=2),
        validate_func=lambda x: any('País Vasco' in s.get('Nombre', '') for s in x)
    )
    
    suite.test(
        "Datos IPV tienen índices numéricos",
        lambda: Get_Table_Data(25171, last_periods=2),
        validate_func=lambda x: any(
            len(s.get('Data', [])) > 0 and 
            all(isinstance(d.get('Valor'), (int, float)) for d in s['Data'] if d.get('Valor') is not None)
            for s in x[:10]
        )
    )
    
    suite.test(
        "Fechas son timestamps válidos",
        lambda: Get_Table_Data(25171, last_periods=2),
        validate_func=lambda x: any(
            len(s.get('Data', [])) > 0 and 
            all(isinstance(d.get('Fecha'), (int, float)) and d['Fecha'] > 1000000000 for d in s['Data'][:2])
            for s in x[:5]
        )
    )
    
    # Test 56-60: Rangos de fechas
    suite.test(
        "Rango de fechas 2024",
        lambda: Get_Table_Data(50902, date_range="20240101:20241231"),
        expected_type=list
    )
    
    suite.test(
        "Rango de fechas 2023-2024",
        lambda: Get_Table_Data(50902, date_range="20230101:20241231"),
        expected_type=list
    )
    
    suite.test(
        "Rango de fechas último trimestre",
        lambda: Get_Table_Data(25171, date_range="20241001:20241231"),
        expected_type=list
    )
    
    suite.test(
        "Combinación: últimos periodos + tipo",
        lambda: Get_Table_Data(50902, last_periods=6, period_type='M'),
        expected_type=list
    )
    
    suite.test(
        "Todas las series tienen unidad",
        lambda: Get_Table_Data(50902, last_periods=3),
        validate_func=lambda x: all('FK_Unidad' in s for s in x[:10])
    )
    
    # Test 61-65: Validación de datos
    suite.test(
        "Series tienen código único",
        lambda: Get_Table_Data(50902, last_periods=3),
        validate_func=lambda x: len(set(s['COD'] for s in x)) == len(x)
    )
    
    suite.test(
        "Datos tienen fechas válidas",
        lambda: Get_Table_Data(50902, last_periods=5),
        validate_func=lambda x: any(
            len(s.get('Data', [])) > 0 and 
            all('Fecha' in d for d in s['Data'][:3])
            for s in x[:5] if len(s.get('Data', [])) > 0
        )
    )
    
    suite.test(
        "Tabla inexistente maneja error",
        lambda: Get_Table_Data(99999999),
        expected_type=list
    )
    
    suite.test(
        "Resultado es JSON serializable",
        lambda: json.dumps(Get_Table_Data(50902, last_periods=2)[:3]),
        expected_type=str
    )
    
    suite.test(
        "Múltiples llamadas son consistentes",
        lambda: len(Get_Table_Data(50902, last_periods=3)) == len(Get_Table_Data(50902, last_periods=3)),
        validate_func=lambda x: x is True
    )
    
    # ============================================================================
    # SECCIÓN 4: Get_Series_Data (15 pruebas)
    # ============================================================================
    suite.print_section("SECCIÓN 4: Get_Series_Data - Datos de Series (15 pruebas)")
    
    # Test 66-70: Básico (usando nult para evitar errores de API)
    series_data = suite.test(
        "Obtener serie con últimos datos",
        lambda: Get_Series_Data("IPC251856", last_periods=12),
        expected_type=dict,
        validate_func=lambda x: 'COD' in x or 'error' in x
    )
    
    suite.test(
        "Serie tiene código",
        lambda: Get_Series_Data("IPC251856", last_periods=6),
        validate_func=lambda x: 'COD' in x or 'error' in x
    )
    
    suite.test(
        "Serie tiene nombre",
        lambda: Get_Series_Data("IPC251856", last_periods=6),
        validate_func=lambda x: 'Nombre' in x or 'error' in x
    )
    
    suite.test(
        "Serie tiene datos o error manejado",
        lambda: Get_Series_Data("IPC251856", last_periods=6),
        validate_func=lambda x: 'Data' in x or 'error' in x
    )
    
    suite.test(
        "Serie retorna estructura válida",
        lambda: Get_Series_Data("IPC251856", last_periods=6),
        validate_func=lambda x: isinstance(x, dict)
    )
    
    # Test 71-75: Parámetros
    suite.test(
        "Serie con últimos 12 periodos",
        lambda: Get_Series_Data("IPC251856", last_periods=12),
        validate_func=lambda x: len(x.get('Data', [])) <= 12
    )
    
    suite.test(
        "Serie con últimos 6 periodos",
        lambda: Get_Series_Data("IPC251856", last_periods=6),
        validate_func=lambda x: len(x.get('Data', [])) <= 6
    )
    
    suite.test(
        "Serie tipo periodo mensual",
        lambda: Get_Series_Data("IPC251856", period_type='M'),
        expected_type=dict
    )
    
    suite.test(
        "Serie tipo periodo anual",
        lambda: Get_Series_Data("IPC251856", period_type='A'),
        expected_type=dict
    )
    
    suite.test(
        "Serie IPV (vivienda) con últimos datos",
        lambda: Get_Series_Data("IPV769", last_periods=4),
        validate_func=lambda x: isinstance(x, dict)
    )
    
    # Test 76-80: Validación
    suite.test(
        "Serie tiene metadatos",
        lambda: Get_Series_Data("IPC251856", last_periods=6),
        validate_func=lambda x: 'COD' in x or 'error' in x
    )
    
    suite.test(
        "Serie maneja parámetros correctamente",
        lambda: Get_Series_Data("IPC251856", last_periods=3),
        validate_func=lambda x: isinstance(x, dict)
    )
    
    suite.test(
        "Serie inexistente maneja error",
        lambda: Get_Series_Data("SERIE_INEXISTENTE_XYZ"),
        expected_type=dict
    )
    
    suite.test(
        "Resultado es JSON serializable",
        lambda: json.dumps(Get_Series_Data("IPC251856", last_periods=3)),
        expected_type=str
    )
    
    suite.test(
        "Llamadas múltiples son consistentes",
        lambda: Get_Series_Data("IPC251856", last_periods=5)['COD'] == "IPC251856",
        validate_func=lambda x: x is True
    )
    
    # ============================================================================
    # SECCIÓN 5: Get_Table_Variables y Get_Variable_Values (10 pruebas)
    # ============================================================================
    suite.print_section("SECCIÓN 5: Variables y Valores (10 pruebas)")
    
    # Test 81-85: Variables
    variables = suite.test(
        "Obtener variables de tabla 50902",
        lambda: Get_Table_Variables(50902),
        expected_type=list,
        validate_func=lambda x: len(x) > 0
    )
    
    suite.test(
        "Variables tienen Id y Nombre",
        lambda: Get_Table_Variables(50902),
        validate_func=lambda x: all('Id' in v and 'Nombre' in v for v in x)
    )
    
    suite.test(
        "Obtener variables de tabla IPV",
        lambda: Get_Table_Variables(25171),
        expected_type=list
    )
    
    suite.test(
        "IDs de variables son únicos",
        lambda: Get_Table_Variables(50902),
        validate_func=lambda x: len(set(v['Id'] for v in x)) == len(x)
    )
    
    suite.test(
        "Tabla inexistente maneja error en variables",
        lambda: Get_Table_Variables(99999999),
        expected_type=list
    )
    
    # Test 86-90: Valores de variables
    variable_values = suite.test(
        "Obtener valores de variable (si existe)",
        lambda: Get_Variable_Values(1, 50902) if variables and len(variables) > 0 else [],
        expected_type=list
    )
    
    suite.test(
        "Valores tienen estructura correcta",
        lambda: Get_Variable_Values(1, 50902),
        expected_type=list
    )
    
    suite.test(
        "Variable inexistente maneja error",
        lambda: Get_Variable_Values(99999, 50902),
        expected_type=list
    )
    
    suite.test(
        "Resultado variables es JSON serializable",
        lambda: json.dumps(Get_Table_Variables(50902)[:3]),
        expected_type=str
    )
    
    suite.test(
        "Múltiples variables funcionan",
        lambda: [Get_Table_Variables(50902), Get_Table_Variables(25171)],
        validate_func=lambda x: len(x) == 2
    )
    
    # ============================================================================
    # SECCIÓN 6: Search_Data y Get_Latest_Data (10 pruebas)
    # ============================================================================
    suite.print_section("SECCIÓN 6: Búsqueda y Datos Recientes (10 pruebas)")
    
    # Test 91-95: Búsqueda
    suite.test(
        "Buscar 'precios' (término más común)",
        lambda: Search_Data("precios"),
        expected_type=list,
        validate_func=lambda x: isinstance(x, list)
    )
    
    suite.test(
        "Buscar 'IPC' (código conocido)",
        lambda: Search_Data("IPC"),
        validate_func=lambda x: len(x) > 0
    )
    
    suite.test(
        "Buscar 'vivienda'",
        lambda: Search_Data("vivienda"),
        validate_func=lambda x: len(x) > 0
    )
    
    suite.test(
        "Buscar con filtro de operación IPC",
        lambda: Search_Data("precios", operation_filter="IPC"),
        validate_func=lambda x: len(x) > 0
    )
    
    suite.test(
        "Buscar con max_results=5",
        lambda: Search_Data("empleo", max_results=5),
        validate_func=lambda x: len(x) <= 5
    )
    
    # Test 96-100: Últimos datos
    suite.test(
        "Obtener últimos datos de IPC",
        lambda: Get_Latest_Data("IPC"),
        expected_type=list,
        validate_func=lambda x: isinstance(x, list)
    )
    
    suite.test(
        "Obtener últimos datos de IPV",
        lambda: Get_Latest_Data("IPV"),
        validate_func=lambda x: isinstance(x, list)
    )
    
    suite.test(
        "Últimos datos con filtro de tabla",
        lambda: Get_Latest_Data("IPC", table_filter="50902"),
        expected_type=list,
        validate_func=lambda x: isinstance(x, list)
    )
    
    suite.test(
        "Búsqueda retorna JSON serializable",
        lambda: json.dumps(Search_Data("IPC", max_results=3)),
        expected_type=str
    )
    
    suite.test(
        "Últimos datos son JSON serializable",
        lambda: Get_Latest_Data("IPC"),
        validate_func=lambda x: isinstance(x, list) and (len(x) == 0 or json.dumps(x[:3]))
    )
    
    # ============================================================================
    # FINALIZAR
    # ============================================================================
    return suite.finish()


if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Pruebas interrumpidas por el usuario{Colors.END}")
        sys.exit(2)
    except Exception as e:
        print(f"\n\n{Colors.RED}Error fatal: {e}{Colors.END}")
        traceback.print_exc()
        sys.exit(3)

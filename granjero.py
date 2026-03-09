from simpleai.search import SearchProblem, breadth_first


class WolfSheepCabbage(SearchProblem):
    def __init__(self):
        super().__init__((0, 0, 0, 0))
        print("=" * 60)
        print("PROBLEMA: Lobo, Cabra y Col")
        print("=" * 60)
        print("Estado: (Granjero, Lobo, Cabra, Col)")
        print("0 = Orilla Izquierda | 1 = Orilla Derecha\n")


    def is_goal(self, state):
        return state == (1, 1, 1, 1)


    def actions(self, state):
        """Genera acciones posibles"""
        actions = []
        f, w, s, c = state
        
        # El granjero siempre puede intentar cruzar solo
        actions.append('F')
        
        # Solo puede llevar lo que está en su misma orilla
        if f == w: actions.append('FW')
        if f == s: actions.append('FS')
        if f == c: actions.append('FC')
        
        return actions


    def result(self, state, action):
        """Aplica una acción y devuelve el nuevo estado"""
        f, w, s, c = state
        nf = 1 - f  # Nueva posición del granjero
        
        if action == 'F':
            return (nf, w, s, c)
        elif action == 'FW':
            return (nf, nf, s, c)
        elif action == 'FS':
            return (nf, w, nf, c)
        elif action == 'FC':
            return (nf, w, s, nf)


    def is_valid(self, state):
        """Verifica si un estado es seguro"""
        f, w, s, c = state
        
        # El lobo come a la cabra si están juntos sin el granjero
        if w == s and f != w:
            return False
        
        # La cabra come la col si están juntas sin el granjero
        if s == c and f != s:
            return False
        
        return True


    def cost(self, state, action, state2):
        return 1


    def successors(self, state):
        """Genera sucesores válidos"""
        for action in self.actions(state):
            new_state = self.result(state, action)
            if self.is_valid(new_state):
                yield (action, new_state, 1)


    def visualize_state(self, state):
        """Visualiza el estado actual"""
        f, w, s, c = state
        
        left = []
        if f == 0: left.append("🧑‍🌾")
        if w == 0: left.append("🐺")
        if s == 0: left.append("🐑")
        if c == 0: left.append("🥬")
        
        right = []
        if f == 1: right.append("🧑‍🌾")
        if w == 1: right.append("🐺")
        if s == 1: right.append("🐑")
        if c == 1: right.append("🥬")
        
        left_str = " ".join(left) if left else "vacío"
        right_str = " ".join(right) if right else "vacío"
        
        return f"  Izq: {left_str:20} ~~~🌊~~~ Der: {right_str}"


    def format_action(self, action):
        names = {
            'F': 'Granjero solo',
            'FW': 'Granjero + Lobo',
            'FS': 'Granjero + Cabra',
            'FC': 'Granjero + Col',
            None: 'Estado inicial'
        }
        return names.get(action, action)


# ==================== EJECUCIÓN ====================

print("\nBuscando solución con Búsqueda en Anchura (BPA)...\n")

problem = WolfSheepCabbage()
result = breadth_first(problem)

if result:
    path = result.path()
    
    print("=" * 60)
    print(f"✓ SOLUCIÓN ENCONTRADA ({len(path) - 1} pasos)")
    print("=" * 60)
    
    for i, (action, state) in enumerate(path):
        print(f"\nPaso {i}: {problem.format_action(action)}")
        print(f"  Estado: {state}")
        print(problem.visualize_state(state))
        
        # Verificar validez
        if not problem.is_valid(state):
            print("  ⚠️  ADVERTENCIA: Este estado es INVÁLIDO")
    
    print("\n" + "=" * 60)
    print("VERIFICACIÓN DE LA SOLUCIÓN:")
    print("=" * 60)
    
    all_valid = True
    for i, (action, state) in enumerate(path):
        valid = problem.is_valid(state)
        status = "✓" if valid else "✗"
        print(f"  {status} Paso {i}: {state} - {problem.format_action(action)}")
        if not valid:
            all_valid = False
    
    if all_valid:
        print("\n✓ Todos los estados son válidos")
    else:
        print("\n✗ La solución contiene estados inválidos")
    
    print("=" * 60)

else:
    print("✗ No se encontró solución")

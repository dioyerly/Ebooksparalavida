# Paletas de Colores por Marca

## Marca 1: Ebooks para la vida

### Identidad
Calidez, bienestar, naturalidad. Estética spa/wellness.

### Paleta Principal

| Color | Hex | RGB | Uso |
|-------|-----|-----|-----|
| Beige Cálido | `#F5E6D3` | 245, 230, 211 | Fondo principal |
| Teal Profundo | `#2A7F7E` | 42, 127, 126 | Headers, botones CTA |
| Coral Suave | `#E8A89F` | 232, 168, 159 | Accents, hover |
| Gris Oscuro | `#3A3A3A` | 58, 58, 58 | Texto principal |
| Blanco | `#FFFFFF` | 255, 255, 255 | Fondo cards |

### CSS Variables

```css
:root.theme-ebooks {
  --primary: #2A7F7E;
  --secondary: #E8A89F;
  --background: #F5E6D3;
  --text: #3A3A3A;
  --light: #FFFFFF;
  --accent: #E8A89F;
}
```

### Tipografía
- Headings: Serif (Georgia, serif)
- Body: Sans-serif (Inter, sans-serif)

---

## Marca 2: YOYI'R

### Identidad
Minimalismo estético, creatividad visual. Agendas y planners.

### Paleta Principal

| Color | Hex | RGB | Uso |
|-------|-----|-----|-----|
| Lavanda Pastel | `#E5D9F0` | 229, 217, 240 | Fondo principal |
| Morado Oscuro | `#7B4D8F` | 123, 77, 143 | Headers, botones |
| Morado Claro | `#D4A5D9` | 212, 165, 217 | Accents, hover |
| Negro Suave | `#2D2D2D` | 45, 45, 45 | Texto principal |
| Blanco | `#FFFFFF` | 255, 255, 255 | Fondo cards |

### CSS Variables

```css
:root.theme-yoyir {
  --primary: #7B4D8F;
  --secondary: #D4A5D9;
  --background: #E5D9F0;
  --text: #2D2D2D;
  --light: #FFFFFF;
  --accent: #D4A5D9;
}
```

### Tipografía
- Headings: Sans-serif Bold (Montserrat, sans-serif)
- Body: Sans-serif (Poppins, sans-serif)

---

## Marca 3: EstrategIA

### Identidad
Tecnología, datos, futurismo. Oscura, edgy, neón.

### Paleta Principal

| Color | Hex | RGB | Uso |
|-------|-----|-----|-----|
| Negro Profundo | `#0A0E27` | 10, 14, 39 | Fondo principal |
| Azul Neón | `#00D9FF` | 0, 217, 255 | Headers, botones, accents |
| Magenta Neón | `#FF00FF` | 255, 0, 255 | Highlights, efectos |
| Gris Oscuro | `#1A1A2E` | 26, 26, 46 | Cards, elementos secundarios |
| Blanco | `#E0E0E0` | 224, 224, 224 | Texto principal |

### CSS Variables

```css
:root.theme-estrategia {
  --primary: #00D9FF;
  --secondary: #FF00FF;
  --background: #0A0E27;
  --text: #E0E0E0;
  --light: #1A1A2E;
  --accent: #00D9FF;
  --glow: #FF00FF;
}
```

### Tipografía
- Headings: Monospace Bold (Courier New, monospace)
- Body: Monospace (IBM Plex Mono, monospace)

### Efectos Especiales
- Glow en botones: `text-shadow: 0 0 10px #00D9FF;`
- Bordes neón: `border: 2px solid #00D9FF; box-shadow: 0 0 10px #00D9FF;`

---

## Home (Página Unificada)

### Paleta Neutra

| Color | Hex | Uso |
|-------|-----|-----|
| Blanco Puro | `#FFFFFF` | Fondo |
| Gris Oscuro | `#2C2C2C` | Texto |
| Gris Claro | `#F0F0F0` | Dividers |
| Azul Corporativo | `#1E40AF` | Enlaces, CTA |

### Efecto de Transición
- Cuando el usuario entra a cada marca, la paleta **transiciona fluidamente** de la paleta neutra a la paleta de la marca.
- Duración: 0.5s - 1s
- Ease: cubic-bezier(0.25, 0.46, 0.45, 0.94)

---

## Implementación en CSS

### Global (Siempre aplicado)

```css
:root {
  --primary: #1E40AF;
  --secondary: #F0F0F0;
  --background: #FFFFFF;
  --text: #2C2C2C;
  --light: #FFFFFF;
}

body {
  background-color: var(--background);
  color: var(--text);
  transition: background-color 0.5s, color 0.5s;
}
```

### Por Tema (Condicional)

```css
/* En theme-ebooks.css */
body.theme-ebooks {
  --primary: #2A7F7E;
  --secondary: #E8A89F;
  --background: #F5E6D3;
  --text: #3A3A3A;
}

/* En theme-yoyir.css */
body.theme-yoyir {
  --primary: #7B4D8F;
  --secondary: #D4A5D9;
  --background: #E5D9F0;
  --text: #2D2D2D;
}

/* En theme-estrategia.css */
body.theme-estrategia {
  --primary: #00D9FF;
  --secondary: #FF00FF;
  --background: #0A0E27;
  --text: #E0E0E0;
}
```

---

## Ejemplos de Uso en HTML

```html
<body class="theme-ebooks">
  <header style="background-color: var(--primary); color: var(--light);">
    Header Teal
  </header>
  <button style="background-color: var(--secondary);">
    CTA Coral
  </button>
</body>
```

---

## Notas de Accesibilidad

- Ratio de contraste mínimo AA (WCAG 2.1): 4.5:1
- Todos los colores primarios vs. texto cumplen este estándar
- No depender solo del color para transmitir información

---

## Recursos Externos

- Color Picker: https://coolors.co
- Contrast Checker: https://webaim.org/resources/contrastchecker/
- Google Fonts: serif, sans-serif, monospace

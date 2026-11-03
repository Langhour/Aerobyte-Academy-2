// AeroByte Academy Official Products Catalog
// Tailored with brands, variants, gallery viewpoints, and technical specifications

export const categoryList = [
  'Student Lab Kits',
  'FPV Drone Hardware',
  'Microcontrollers & Sensors',
  'Brushless Motors & ESCs',
  'Tools & Equipment',
  '3D Filaments & Parts'
]

export const products = [
  {
    id: 'starter-robotics-kit',
    brand: 'AeroByte Lab',
    brandLogo: '🤖',
    brandRating: '4.9 ★ (5.5K)',
    name: 'Starter Robotics Lab Kit (ESP32 Edition)',
    category: 'Student Lab Kits',
    priceUsd: 45.0,
    rating: 5.0,
    reviewsCount: '5.5K',
    badge: 'BEST SELLER',
    badgeType: 'tiktok',
    awardBadge: true,
    awardTitle: 'AEROBYTE LAB',
    awardSubtitle: 'BEST MAKER KIT 2026',
    inStock: true,
    stockCount: 14,
    icon: '🤖',
    colorOptions: [
      { name: 'Standard Blue', colorClass: 'bg-blue-600', icon: '🤖' },
      { name: 'Stealth Black', colorClass: 'bg-slate-900', icon: '🦾' },
      { name: 'Cyber Orange', colorClass: 'bg-amber-500', icon: '🏎️' }
    ],
    sizeOptions: ['Standard Kit', 'Pro with Sensors'],
    gallery: [
      { label: 'Overview', icon: '🤖', title: 'Complete Robotic Chassis Assembly' },
      { label: 'MCU Shield', icon: '📟', title: 'ESP32 Dual-Core Wireless Controller' },
      { label: 'Sensors', icon: '📡', title: 'Ultrasonic Obstacle Avoidance Sensor' },
      { label: 'Motors', icon: '⚙️', title: 'Dual Metal Gear DC Motors & Wheels' },
      { label: 'Lab Box', icon: '📦', title: 'Official AeroByte Academy Foam-Padded Box' }
    ],
    description: 'All-in-one learning kit with ESP32 board, dual motor driver shield, ultrasonic sensors, chassis, servo, and breadboard wires. Engineered specifically for students and makers starting autonomous robotics.',
    longDescription: 'The AeroByte Starter Robotics Lab Kit is Cambodia\'s premier hands-on education platform for learning embedded C++, IoT telemetry, and obstacle-avoidance algorithms. Driven by the powerful dual-core ESP32 microcontroller, students can stream telemetry via Wi-Fi and Bluetooth directly to their smartphone or PC dashboard.',
    whatsInBox: [
      '1x ESP32 Dual-Core 240MHz Development Board',
      '1x L298N Dual H-Bridge Motor Driver Shield',
      '1x HC-SR04 Ultrasonic Distance Sensor with mount',
      '1x Micro Servo SG90 (180-degree rotation)',
      '2x High-torque TT Motors with Rubber Grip Wheels',
      '1x Heavy-duty Laser Cut Acrylic Chassis Platform',
      '1x 18650 Dual-Slot Battery Box & Jumper Wire Bundle'
    ],
    tags: ['ESP32', 'Robotics', 'Lab Ready', 'Wi-Fi Telemetry'],
    specs: {
      'MCU': 'ESP32 Dual-Core 240MHz',
      'Connectivity': 'Wi-Fi 802.11 b/g/n + BLE 4.2',
      'Motor Driver': 'Dual H-Bridge L298N Shield',
      'Chassis': 'Laser-cut Acrylic Smart Car Platform',
      'Battery Support': '2x 18650 Li-ion cells (7.4V input)',
      'Weight': '380g assembled'
    }
  },
  {
    id: 'iot-maker-kit',
    brand: 'AeroByte Lab',
    brandLogo: '💡',
    brandRating: '4.8 ★ (1.7K)',
    name: 'Advanced Arduino IoT Maker Kit',
    category: 'Student Lab Kits',
    priceUsd: 35.0,
    rating: 4.9,
    reviewsCount: '1.7K',
    badge: 'LAB FAVORITE',
    badgeType: 'normal',
    awardBadge: false,
    awardTitle: 'STEM APPROVED',
    awardSubtitle: 'BEGINNER FRIENDLY',
    inStock: true,
    stockCount: 18,
    icon: '💡',
    colorOptions: [
      { name: 'Standard Edition', colorClass: 'bg-emerald-600', icon: '💡' },
      { name: 'Deluxe Storage Box', colorClass: 'bg-slate-800', icon: '🧰' }
    ],
    sizeOptions: ['Standard (30+ Components)', 'Deluxe (50+ Components)'],
    gallery: [
      { label: 'Master Kit', icon: '💡', title: 'Complete IoT Sensor Suite' },
      { label: 'Controller', icon: '🔌', title: 'Arduino Uno Compatible Board' },
      { label: 'Display', icon: '📟', title: '0.96 inch I2C High-Contrast OLED' },
      { label: 'Sensors', icon: '🌡️', title: 'DHT11 Temp & Humidity + PIR Sensors' },
      { label: 'Carrying Case', icon: '💼', title: 'Double-Layer Plastic Organizer Case' }
    ],
    description: 'Arduino Uno compatible controller, OLED display, DHT11 temp/humidity sensor, relay module, and 30+ components for IoT projects and smart home automation.',
    longDescription: 'Designed for STEM academies and high school coding workshops, this kit provides everything required to build real-time smart home devices, weather stations, and automated plant watering systems with step-by-step schematics.',
    whatsInBox: [
      '1x ATmega328P Uno Compatible Board with USB cable',
      '1x 0.96" I2C OLED 128x64 display',
      '1x DHT11 Digital Temperature & Humidity Sensor',
      '1x PIR Motion Detection Sensor',
      '1x 5V Single Channel Relay Module',
      '1x 830-Point Solderless Breadboard & 65x Jumper Wires',
      'Assorted LEDs, Resistors, Buttons, and Buzzer'
    ],
    tags: ['Arduino', 'Sensors', 'Beginner', 'Smart Home'],
    specs: {
      'Controller': 'ATmega328P Uno Compatible (16MHz)',
      'Display': '0.96" I2C OLED (128x64 pixels)',
      'Sensors': 'DHT11, PIR Motion, Light LDR',
      'Operating Voltage': '5V DC via USB or External DC Jack'
    }
  },
  {
    id: 'drone-frame-5in',
    brand: 'Aero Fly',
    brandLogo: '🚁',
    brandRating: '4.8 ★ (900)',
    name: '5" FPV Racing Drone Frame (Carbon Fiber)',
    category: 'FPV Drone Hardware',
    priceUsd: 29.0,
    rating: 4.8,
    reviewsCount: '900',
    badge: '3K CARBON',
    badgeType: 'normal',
    awardBadge: true,
    awardTitle: 'AERO FLY',
    awardSubtitle: 'RACE CERTIFIED',
    inStock: true,
    stockCount: 9,
    icon: '🚁',
    colorOptions: [
      { name: 'Matte Raw Carbon', colorClass: 'bg-neutral-900', icon: '🚁' },
      { name: 'Chameleon Titanium', colorClass: 'bg-purple-900', icon: '🛸' }
    ],
    sizeOptions: ['5 Inch (225mm)', '6 Inch Long Range'],
    gallery: [
      { label: 'Frame', icon: '🚁', title: 'Toray 3K Matte Carbon Fiber Chassis' },
      { label: 'Arms', icon: '📐', title: '5.0mm Chamfered True-X Racing Arms' },
      { label: 'Camera Cage', icon: '🎥', title: 'CNC Aluminum Action Cam Mount' },
      { label: 'Hardware', icon: '🔩', title: 'Grade 12.9 High-Tensile Steel Screws' }
    ],
    description: '3K pure matte carbon fiber, 5mm arms, lightweight aerodynamic racing frame designed for 2207 brushless motors and high-speed freestyle maneuvers.',
    longDescription: 'Crafted with premium Japanese Toray 3K carbon weave, the Aero Fly 5" Racing Frame delivers ultra-rigid vibration absorption, allowing your flight controller PID loops to run clean without motor oscillations.',
    whatsInBox: [
      '4x 5mm Chamfered Carbon Fiber Replacement Arms',
      '1x 2.5mm Carbon Fiber Top Plate & 2mm Bottom Plate',
      '1x Set of 30mm Textured Aluminum Standoffs',
      '1x Non-slip Silicone Battery Grip Pad',
      '1x High-durability Kevlar Battery Strap',
      '1x 3D-Printed TPU Action Cam Angle Mount'
    ],
    tags: ['FPV', 'Carbon Fiber', 'Racing', 'Freestyle'],
    specs: {
      'Material': 'Toray 3K Matte Carbon Fiber',
      'Wheelbase': '225mm True-X Geometry',
      'Arm Thickness': '5.0mm Chamfered Edges',
      'Stack Mounting': '20x20mm & 30.5x30.5mm',
      'Weight': '112g with hardware'
    }
  },
  {
    id: 'f405-esc-stack',
    brand: 'Aero Fly',
    brandLogo: '⚡',
    brandRating: '4.9 ★ (92.1K)',
    name: 'F405 V3 Flight Controller + 50A 4-in-1 ESC',
    category: 'FPV Drone Hardware',
    priceUsd: 62.0,
    rating: 4.9,
    reviewsCount: '92.1K',
    badge: 'FLAGSHIP',
    badgeType: 'normal',
    awardBadge: true,
    awardTitle: 'PRO PILOT',
    awardSubtitle: '6S READY STACK',
    inStock: true,
    stockCount: 7,
    icon: '⚡',
    colorOptions: [
      { name: 'Standard Black PCB', colorClass: 'bg-black', icon: '⚡' }
    ],
    sizeOptions: ['30.5x30.5mm (Standard)', '20x20mm (Mini)'],
    gallery: [
      { label: 'Stack Top', icon: '⚡', title: 'STM32F405 Flight Controller Board' },
      { label: 'ESC Bottom', icon: '🔋', title: '50A BLHeli_S 4-in-1 ESC Board' },
      { label: 'Connectors', icon: '🔌', title: 'DJI O3 / Caddx Vista Plug-and-Play' },
      { label: 'Capacitor', icon: '🧲', title: 'Low ESR Rubycon Filter Capacitor' }
    ],
    description: 'Betaflight OSD, barometer, blackbox logging, 3-6S LiPo input, with BLHeli_S 50A continuous current handling for maximum throttle authority.',
    longDescription: 'The Aero Fly F405 V3 stack offers peak reliability with integrated filtering capacitors and a direct plug-and-play wiring harness for digital HD video transmitters.',
    whatsInBox: [
      '1x F405 V3 Flight Controller Board',
      '1x 50A 4-in-1 BLHeli_S ESC',
      '1x 8-Pin JST-SH Silicon Interconnect Cable',
      '1x Rubycon 35V 1000uF Low-ESR Capacitor',
      '1x XT60 Heavy Duty Pre-tinned Pigtail Cable',
      '4x Anti-vibration M3 Silicone Grommets'
    ],
    tags: ['Flight Controller', 'Betaflight', '6S', 'DJI O3 Compatible'],
    specs: {
      'MCU': 'STM32F405 168MHz',
      'ESC Current': '50A Continuous (60A Burst)',
      'Firmware': 'Betaflight / BLHeli_S',
      'Input Voltage': '3S - 6S LiPo (11.1V - 25.2V)',
      'OSD': 'AT7456E On-Screen Display',
      'Blackbox': '16MB Onboard Flash'
    }
  },
  {
    id: 'brushless-motor-pack',
    brand: 'Aero Fly',
    brandLogo: '⚙️',
    brandRating: '5.0 ★ (41.1K)',
    name: 'Brushless Motor 2207 1950KV (Set of 4)',
    category: 'Brushless Motors & ESCs',
    priceUsd: 54.0,
    rating: 5.0,
    reviewsCount: '41.1K',
    badge: 'POWER EDITION',
    badgeType: 'normal',
    awardBadge: true,
    awardTitle: 'COSMOPOLITAN TECH',
    awardSubtitle: 'MAX THRUST 2026',
    inStock: true,
    stockCount: 11,
    icon: '⚙️',
    colorOptions: [
      { name: 'Cobalt Blue', colorClass: 'bg-blue-700', icon: '⚙️' },
      { name: 'Emerald Teal', colorClass: 'bg-emerald-600', icon: '🌀' },
      { name: 'Obsidian Black', colorClass: 'bg-slate-900', icon: '🖤' }
    ],
    sizeOptions: ['1950KV (6S Freestyle)', '2550KV (4S Racing)'],
    gallery: [
      { label: 'Set of 4', icon: '⚙️', title: 'Quad Matching Brushless Motors' },
      { label: 'Bell Stator', icon: '🌀', title: '2207 Stator with Hollow Titanium Shaft' },
      { label: 'Magnets', icon: '🧲', title: 'N52H Curved Neodymium Magnets' },
      { label: 'Bearings', icon: '🛡️', title: 'Japanese NSK 9x4x4mm High-RPM Bearings' }
    ],
    description: 'High torque hollow titanium shaft, N52H curved magnets, super smooth throttle curve for FPV freestyle and racing.',
    longDescription: 'Engineered for high dynamic response, these 2207 brushless motors deliver exceptional cooling, instant cornering torque, and silky-smooth low-end control.',
    whatsInBox: [
      '4x 2207 1950KV Brushless Motors (pre-soldered wires)',
      '4x Aluminum Anodized M5 Flanged Locknuts',
      '16x M3x7mm High-Strength Motor Screws'
    ],
    tags: ['6S Motors', 'High Torque', 'Titanium Shaft', 'NSK Bearings'],
    specs: {
      'Stator Size': '2207 (Titanium Shaft)',
      'KV Rating': '1950KV (Optimized for 6S)',
      'Max Thrust': '1,920g per motor',
      'Shaft Diameter': '5mm M5 Thread',
      'Weight': '33.5g per motor'
    }
  },
  {
    id: 'esp32-dual-core',
    brand: 'Espressif',
    brandLogo: '📡',
    brandRating: '4.9 ★ (12.4K)',
    name: 'ESP32-WROOM-32D Development Board',
    category: 'Microcontrollers & Sensors',
    priceUsd: 6.5,
    rating: 4.9,
    reviewsCount: '12.4K',
    badge: 'TOP SELLER',
    badgeType: 'normal',
    awardBadge: false,
    awardTitle: 'OFFICIAL ESP',
    awardSubtitle: 'DUAL CORE MCU',
    inStock: true,
    stockCount: 42,
    icon: '📡',
    colorOptions: [
      { name: 'Standard Type-C', colorClass: 'bg-slate-800', icon: '📡' },
      { name: 'Header Pre-Soldered', colorClass: 'bg-indigo-700', icon: '🔌' }
    ],
    sizeOptions: ['30-Pin Type-C', '38-Pin Micro-USB'],
    gallery: [
      { label: 'Board Front', icon: '📡', title: 'ESP32 Development Board Front View' },
      { label: 'Type-C Port', icon: '⚡', title: 'Modern Reversible USB Type-C' },
      { label: 'Pinout Diagram', icon: '📐', title: 'Breadboard Compatible Pinout' },
      { label: 'Antenna', icon: '📶', title: 'Onboard 2.4GHz PCB Trace Antenna' }
    ],
    description: '2.4GHz Wi-Fi + Bluetooth BLE dual-core MCU, modern Type-C interface, breadboard friendly pinout.',
    longDescription: 'The quintessential IoT platform worldwide. Runs MicroPython, Arduino IDE, FreeRTOS, and ESP-IDF with ultra-low sleep current.',
    whatsInBox: [
      '1x ESP32-WROOM-32D Board with USB Type-C',
      '2x 15-Pin Male Headers (pre-soldered)'
    ],
    tags: ['Wi-Fi', 'Bluetooth', 'Type-C', 'Dual-Core'],
    specs: {
      'Processor': 'Xtensa Dual-Core 32-bit LX6 240MHz',
      'USB Port': 'Modern USB Type-C (CH340 Driver)',
      'GPIO': '30 General-Purpose I/O Pins',
      'Memory': '520KB SRAM + 4MB SPI Flash'
    }
  },
  {
    id: 'raspberry-pi-4',
    brand: 'Raspberry Pi',
    brandLogo: '🍓',
    brandRating: '4.9 ★ (8.3K)',
    name: 'Raspberry Pi 4 Model B (4GB RAM)',
    category: 'Microcontrollers & Sensors',
    priceUsd: 68.0,
    rating: 4.9,
    reviewsCount: '8.3K',
    badge: 'OFFICIAL',
    badgeType: 'normal',
    awardBadge: true,
    awardTitle: 'RASPBERRY PI',
    awardSubtitle: 'AUTHENTIC HARDWARE',
    inStock: true,
    stockCount: 6,
    icon: '🍓',
    colorOptions: [
      { name: 'Standard Board Only', colorClass: 'bg-emerald-700', icon: '🍓' },
      { name: 'With Aluminum Armor Case', colorClass: 'bg-slate-900', icon: '🛡️' }
    ],
    sizeOptions: ['4GB LPDDR4', '8GB LPDDR4'],
    gallery: [
      { label: 'Board Top', icon: '🍓', title: 'Authentic UK Raspberry Pi 4' },
      { label: 'Ports View', icon: '🔌', title: 'Dual Micro-HDMI, Gigabit & USB 3.0' },
      { label: 'Processor', icon: '🧠', title: 'Broadcom BCM2711 Quad-Core SoC' },
      { label: 'Box Packaging', icon: '📦', title: 'Official Raspberry Pi Foundation Box' }
    ],
    description: 'Quad-core 64-bit ARM Cortex-A72, dual 4K micro-HDMI, Gigabit Ethernet, USB 3.0 for computer vision & autonomous drones.',
    longDescription: 'Ideal for autonomous drone path-planning, ROS (Robot Operating System), onboard OpenCV image detection, and localized edge AI.',
    whatsInBox: [
      '1x Authentic Raspberry Pi 4 Model B (4GB RAM)',
      '1x Official Quick-Start Safety Guide'
    ],
    tags: ['AI / Vision', 'Linux', 'ROS', 'Gigabit Ethernet'],
    specs: {
      'Processor': 'Quad-Core 1.5GHz 64-bit Cortex-A72',
      'RAM': '4GB LPDDR4-3200 SDRAM',
      'Video': 'Dual Micro-HDMI Ports (up to 4Kp60)',
      'Connectivity': 'Gigabit Ethernet + 5GHz Wi-Fi + BLE 5.0'
    }
  },
  {
    id: 'digital-soldering-station',
    brand: 'Aero Tools',
    brandLogo: '🔥',
    brandRating: '4.9 ★ (3.1K)',
    name: 'Precision Digital Soldering Iron (65W)',
    category: 'Tools & Equipment',
    priceUsd: 38.0,
    rating: 4.9,
    reviewsCount: '3.1K',
    badge: 'HOT CHOICE',
    badgeType: 'normal',
    awardBadge: true,
    awardTitle: 'COSMOPOLITAN TECH',
    awardSubtitle: 'BEST LAB TOOL 2026',
    inStock: true,
    stockCount: 15,
    icon: '🔥',
    colorOptions: [
      { name: 'Blush Pink', colorClass: 'bg-pink-300', icon: '🌸' },
      { name: 'Matte Gunmetal', colorClass: 'bg-slate-700', icon: '🔥' },
      { name: 'Deep Navy', colorClass: 'bg-navy-900', icon: '⚡' }
    ],
    sizeOptions: ['Standard 65W PD', 'Pro 100W QuickCharge'],
    gallery: [
      { label: 'Front View', icon: '🔥', title: 'Precision Ergonomic 65W Digital Iron' },
      { label: 'OLED Display', icon: '📟', title: '0.96 inch High-Contrast Temperature Monitor' },
      { label: 'Ceramic Core', icon: '⚡', title: '8-Second Rapid Heating to 300°C' },
      { label: 'Silicone Grip', icon: '🧤', title: 'Heat-Resistant Ergonomic Non-Slip Grip' },
      { label: 'Package Kit', icon: '📦', title: 'Retail Metal Carrying Tin & Stand' }
    ],
    description: 'OLED screen, 8-second rapid heating to 300°C, PID temperature stabilization, auto-sleep mode, and ergonomic silicone grip.',
    longDescription: 'Designed for soldering delicate surface-mount components, drone flight controllers, and heavy battery pigtails. Powered directly by standard USB-C PD power banks or wall chargers.',
    whatsInBox: [
      '1x Precision 65W Digital Soldering Iron Handle',
      '1x Fine Chisel Soldering Tip (B2 model)',
      '1x 100W 1.2m Silicone USB-C to USB-C Cable',
      '1x Portable Soldering Iron Stand with Brass Sponge',
      '1x Hex Key & Screw Kit'
    ],
    tags: ['Soldering', 'Lab Grade', 'Type-C PD', 'PID Control'],
    specs: {
      'Power Output': '65W PD / QC Compatible (up to 20V/3.25A)',
      'Heat-up Time': '8 Seconds from 25°C to 300°C',
      'Display': '0.96" OLED Status Screen',
      'Temperature Range': '100°C - 450°C (±2% Accuracy)',
      'Power Port': 'USB Type-C with PD 2.0 / 3.0 Support'
    }
  },
  {
    id: 'lipo-balance-charger',
    brand: 'Aero Tools',
    brandLogo: '🔋',
    brandRating: '4.8 ★ (1.9K)',
    name: 'Smart LiPo Balance Charger (6S 80W)',
    category: 'Tools & Equipment',
    priceUsd: 32.0,
    rating: 4.8,
    reviewsCount: '1.9K',
    badge: null,
    awardBadge: false,
    awardTitle: 'SAFE CHARGE',
    awardSubtitle: 'SMART BALANCE',
    inStock: true,
    stockCount: 12,
    icon: '🔋',
    colorOptions: [
      { name: 'Metallic Blue', colorClass: 'bg-blue-600', icon: '🔋' }
    ],
    sizeOptions: ['80W DC Input', '100W AC/DC Built-in'],
    gallery: [
      { label: 'Charger Front', icon: '🔋', title: 'Backlit LCD Digital Balance Charger' },
      { label: 'Balance Ports', icon: '🔌', title: 'JST-XH Balance Ports for 1S to 6S' },
      { label: 'Cables', icon: '⚡', title: 'XT60, Deans, and Crocodile Clip Cables' }
    ],
    description: 'Supports LiPo, LiFe, Li-ion, NiMH battery packs. Built-in internal resistance meter and storage discharge mode.',
    longDescription: 'Essential for safety when handling high-capacity lithium batteries. Features auto-cutoff, cycle discharge, and balance verification.',
    whatsInBox: [
      '1x Smart 80W Balance Charger Unit',
      '1x DC Input Power Cable with Alligator Clips',
      '1x Multi-Connector Output Cable Harness (XT60, JST, T-Plug)'
    ],
    tags: ['Charger', 'LiPo', 'Safety', 'Balance'],
    specs: {
      'Supported': 'LiPo / LiFe / Li-ion (1-6S), NiMH (1-15S)',
      'Charge Power': '80W (0.1A - 6.0A Adjustable)',
      'Discharge Power': '10W (0.1A - 2.0A Adjustable)',
      'Balance Current': '300mA per cell'
    }
  },
  {
    id: 'aeropla-filament-1kg',
    brand: 'Aero Print',
    brandLogo: '🧵',
    brandRating: '4.9 ★ (6.7K)',
    name: 'AeroPLA Tough 3D Printing Filament (1kg)',
    category: '3D Filaments & Parts',
    priceUsd: 16.0,
    rating: 4.9,
    reviewsCount: '6.7K',
    badge: 'VIRAL',
    badgeType: 'tiktok',
    awardBadge: true,
    awardTitle: 'COSMOPOLITAN TECH',
    awardSubtitle: 'ZERO WARP FILAMENT',
    inStock: true,
    stockCount: 30,
    icon: '🧵',
    colorOptions: [
      { name: 'Signal White', colorClass: 'bg-white border border-slate-300', icon: '⚪' },
      { name: 'Stealth Black', colorClass: 'bg-black', icon: '⚫' },
      { name: 'Aero Blue', colorClass: 'bg-blue-600', icon: '🔵' },
      { name: 'Fire Engine Red', colorClass: 'bg-red-600', icon: '🔴' }
    ],
    sizeOptions: ['1.0 kg (2.2 lbs) Spool', '3.0 kg Bulk Pack'],
    gallery: [
      { label: 'Spool View', icon: '🧵', title: 'Precision Wind 1kg PLA Spool' },
      { label: 'Printed Part', icon: '🖨️', title: 'Ultra-Smooth Layer Adhesion Test' },
      { label: 'Dimensional Check', icon: '📏', title: 'Laser Gauged ±0.02mm Uniform Diameter' },
      { label: 'Vacuum Bag', icon: '📦', title: 'Desiccant Vacuum-Sealed Foil Bag' }
    ],
    description: '1.75mm diameter, high impact resistance, zero warping, optimized for mechanical parts, robotics arms, and drone brackets.',
    longDescription: 'Formulated with modified organic lactide polymers for improved layer-to-layer cohesion, reduced brittleness, and pristine surface sheen.',
    whatsInBox: [
      '1x 1kg (2.2 lbs) AeroPLA Filament Spool',
      '1x High-absorption silica desiccant bag inside vacuum seal'
    ],
    tags: ['PLA', '1kg Spool', '3D Print', 'Zero Warp'],
    specs: {
      'Diameter': '1.75mm (±0.02mm tolerance)',
      'Net Weight': '1.0 kg (2.2 lbs) on Spool',
      'Print Temp': '205°C - 225°C',
      'Bed Temp': '50°C - 60°C (or unheated with glue)'
    }
  },
  {
    id: 'tpu-flexible-filament',
    brand: 'Aero Print',
    brandLogo: '🌀',
    brandRating: '4.8 ★ (1.1K)',
    name: 'TPU Flexible 95A Filament (1kg Elasticity)',
    category: '3D Filaments & Parts',
    priceUsd: 22.0,
    rating: 4.8,
    reviewsCount: '1.1K',
    badge: null,
    awardBadge: false,
    awardTitle: 'ELASTIC GRADE',
    awardSubtitle: 'IMPACT SHOCK',
    inStock: true,
    stockCount: 16,
    icon: '🌀',
    colorOptions: [
      { name: 'Translucent Clear', colorClass: 'bg-slate-200', icon: '⚪' },
      { name: 'Jet Black', colorClass: 'bg-black', icon: '⚫' },
      { name: 'Neon Green', colorClass: 'bg-lime-500', icon: '🟢' }
    ],
    sizeOptions: ['1.0 kg Spool (1.75mm)', '0.5 kg Mini Spool'],
    gallery: [
      { label: 'Spool Front', icon: '🌀', title: '95A Shore Elastic Filament Spool' },
      { label: 'Flex Test', icon: '🤹', title: 'High Tear Strength & 450% Elongation' },
      { label: 'Drone Mount', icon: '🚁', title: 'Printed FPV Goggle & Action Cam Bumper' }
    ],
    description: 'Perfect for FPV drone bumpers, action camera vibration dampeners, robotic gripper pads, and protective sleeves.',
    longDescription: 'Shore 95A provides the sweet spot between easy feeding through direct drive extruders and rubber-like flexibility to withstand crashes.',
    whatsInBox: [
      '1x 1kg TPU 95A Filament on Transparent Spool',
      'Vacuum-sealed packaging with humidity indicator'
    ],
    tags: ['Flexible 95A', 'Crash Proof', 'FPV TPU'],
    specs: {
      'Hardness': 'Shore 95A High Elasticity',
      'Diameter': '1.75mm (±0.03mm precision)',
      'Elongation at Break': '450%',
      'Print Temp': '215°C - 235°C'
    }
  },
  {
    id: 'multimeter-tool-kit',
    brand: 'Aero Tools',
    brandLogo: '🧰',
    brandRating: '4.8 ★ (2.4K)',
    name: 'True-RMS Multimeter & Electronics Tool Kit',
    category: 'Tools & Equipment',
    priceUsd: 26.0,
    rating: 4.8,
    reviewsCount: '2.4K',
    badge: 'KIT VALUE',
    badgeType: 'normal',
    awardBadge: false,
    awardTitle: 'LAB TESTED',
    awardSubtitle: 'CAT III 600V',
    inStock: true,
    stockCount: 14,
    icon: '🧰',
    colorOptions: [
      { name: 'Classic Black & Orange', colorClass: 'bg-amber-600', icon: '🧰' }
    ],
    sizeOptions: ['Complete 7-in-1 Kit'],
    gallery: [
      { label: 'Kit Overview', icon: '🧰', title: 'Full Field Diagnostic & Soldering Tool Kit' },
      { label: 'Multimeter', icon: '📟', title: '6000-Count True-RMS Auto-Ranging Meter' },
      { label: 'Wire Cutters', icon: '✂️', title: 'Flush Japanese Steel Precision Snips' },
      { label: 'Carrying Pouch', icon: '💼', title: 'Shockproof Zippered Storage Case' }
    ],
    description: 'True RMS auto-ranging multimeter, flush wire cutters, ESD anti-static tweezers, desoldering pump, and storage carry case.',
    longDescription: 'Everything required to debug drone electronics, verify solder bridge continuity, measure battery resistance, and assemble lab breadboards.',
    whatsInBox: [
      '1x True-RMS 6000-Count Digital Multimeter',
      '1x Pair Gold-Plated Test Probes',
      '1x Temperature Thermocouple Probe',
      '1x Precision Flush Wire Cutters',
      '2x Anti-Static ESD Tweezers (Straight & Curved)',
      '1x High-Vacuum Desoldering Pump',
      '1x Rugged Canvas Tool Case with Straps'
    ],
    tags: ['Multimeter', 'Tools', 'True RMS', 'ESD Safe'],
    specs: {
      'Multimeter Type': 'True-RMS Auto-Ranging 6000 Counts',
      'Safety Rating': 'CAT III 600V / CAT II 1000V',
      'Measurements': 'DC/AC Voltage, Current, Resistance, Capacitance, Continuity',
      'Display': 'Backlit LCD with Flashlight Function'
    }
  }
]

export function getProductById(id) {
  if (!id) return null
  return products.find(p => p.id === id) || null
}

export function getRelatedProducts(currentId, category, limit = 4) {
  return products
    .filter(p => p.id !== currentId && (p.category === category || !category))
    .slice(0, limit)
}

OPENING_BOOK = {
    # ═══════════════════════════════════════════════════════════════
    # MAIN OPENING CHOICES
    # ═══════════════════════════════════════════════════════════════
    "": ["e2e4", "d2d4", "c2c4", "g1f3"],
    
    # ═══════════════════════════════════════════════════════════════
    # 1.e4 OPENINGS
    # ═══════════════════════════════════════════════════════════════
    
    # ─── E4 MAIN RESPONSES ───
    "e2e4": ["e7e5", "c7c5", "e7e6", "c7c6", "d7d6", "g8f6"],
    
    # ═══════════════════════════════════════════════════════════════
    # 1.e4 e5 - OPEN GAMES
    # ═══════════════════════════════════════════════════════════════
    
    "e2e4 e7e5": ["g1f3", "f1c4", "b1c3"],
    
    # ───────────────────────────────────────────────────────────────
    # ITALIAN GAME (Giuoco Piano) - 10+ moves
    # ───────────────────────────────────────────────────────────────
    "e2e4 e7e5 g1f3": ["b8c6", "g8f6"],
    "e2e4 e7e5 g1f3 b8c6": ["f1c4", "f1b5", "d2d4"],
    
    # Italian Game mainline
    "e2e4 e7e5 g1f3 b8c6 f1c4": ["f8c5", "g8f6", "f8e7"],
    "e2e4 e7e5 g1f3 b8c6 f1c4 f8c5": ["c2c3", "d2d3", "b2b4", "e1g1"],
    
    # Giuoco Piano (c3 system) - DEEP LINE
    "e2e4 e7e5 g1f3 b8c6 f1c4 f8c5 c2c3": ["g8f6", "d8e7"],
    "e2e4 e7e5 g1f3 b8c6 f1c4 f8c5 c2c3 g8f6": ["d2d4", "d2d3"],
    "e2e4 e7e5 g1f3 b8c6 f1c4 f8c5 c2c3 g8f6 d2d4": ["e5d4"],
    "e2e4 e7e5 g1f3 b8c6 f1c4 f8c5 c2c3 g8f6 d2d4 e5d4": ["c3d4"],
    "e2e4 e7e5 g1f3 b8c6 f1c4 f8c5 c2c3 g8f6 d2d4 e5d4 c3d4": ["c5b4"],
    "e2e4 e7e5 g1f3 b8c6 f1c4 f8c5 c2c3 g8f6 d2d4 e5d4 c3d4 c5b4": ["b1c3"],
    "e2e4 e7e5 g1f3 b8c6 f1c4 f8c5 c2c3 g8f6 d2d4 e5d4 c3d4 c5b4 b1c3": ["f6e4"],
    "e2e4 e7e5 g1f3 b8c6 f1c4 f8c5 c2c3 g8f6 d2d4 e5d4 c3d4 c5b4 b1c3 f6e4": ["e1g1"],
    "e2e4 e7e5 g1f3 b8c6 f1c4 f8c5 c2c3 g8f6 d2d4 e5d4 c3d4 c5b4 b1c3 f6e4 e1g1": ["e4c3"],
    "e2e4 e7e5 g1f3 b8c6 f1c4 f8c5 c2c3 g8f6 d2d4 e5d4 c3d4 c5b4 b1c3 f6e4 e1g1 e4c3": ["b2c3"],
    
    # Italian Two Knights Defense
    "e2e4 e7e5 g1f3 b8c6 f1c4 g8f6": ["d2d4", "b1c3", "d2d3"],
    "e2e4 e7e5 g1f3 b8c6 f1c4 g8f6 d2d4": ["e5d4"],
    "e2e4 e7e5 g1f3 b8c6 f1c4 g8f6 d2d4 e5d4": ["e1g1"],
    "e2e4 e7e5 g1f3 b8c6 f1c4 g8f6 d2d4 e5d4 e1g1": ["f6e4"],
    
    # ───────────────────────────────────────────────────────────────
    # RUY LOPEZ (Spanish Opening) - 10+ moves
    # ───────────────────────────────────────────────────────────────
    "e2e4 e7e5 g1f3 b8c6 f1b5": ["a7a6", "g8f6", "f8c5"],
    
    # Morphy Defense (main line)
    "e2e4 e7e5 g1f3 b8c6 f1b5 a7a6": ["b5a4", "b5c6"],
    "e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 b5a4": ["g8f6", "f8c5"],
    "e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 b5a4 g8f6": ["e1g1", "d2d3"],
    "e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 b5a4 g8f6 e1g1": ["f8e7", "f6e4"],
    
    # Closed Ruy Lopez - DEEP LINE
    "e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 b5a4 g8f6 e1g1 f8e7": ["f1e1"],
    "e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 b5a4 g8f6 e1g1 f8e7 f1e1": ["b7b5"],
    "e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 b5a4 g8f6 e1g1 f8e7 f1e1 b7b5": ["a4b3"],
    "e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 b5a4 g8f6 e1g1 f8e7 f1e1 b7b5 a4b3": ["d7d6"],
    "e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 b5a4 g8f6 e1g1 f8e7 f1e1 b7b5 a4b3 d7d6": ["c2c3"],
    "e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 b5a4 g8f6 e1g1 f8e7 f1e1 b7b5 a4b3 d7d6 c2c3": ["e8g8"],
    "e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 b5a4 g8f6 e1g1 f8e7 f1e1 b7b5 a4b3 d7d6 c2c3 e8g8": ["h2h3"],
    "e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 b5a4 g8f6 e1g1 f8e7 f1e1 b7b5 a4b3 d7d6 c2c3 e8g8 h2h3": ["c6a5"],
    "e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 b5a4 g8f6 e1g1 f8e7 f1e1 b7b5 a4b3 d7d6 c2c3 e8g8 h2h3 c6a5": ["b3c2"],
    
    # Berlin Defense
    "e2e4 e7e5 g1f3 b8c6 f1b5 g8f6": ["e1g1", "d2d3"],
    "e2e4 e7e5 g1f3 b8c6 f1b5 g8f6 e1g1": ["f6e4"],
    "e2e4 e7e5 g1f3 b8c6 f1b5 g8f6 e1g1 f6e4": ["d2d4"],
    
    # ───────────────────────────────────────────────────────────────
    # SCOTCH GAME
    # ───────────────────────────────────────────────────────────────
    "e2e4 e7e5 g1f3 b8c6 d2d4": ["e5d4"],
    "e2e4 e7e5 g1f3 b8c6 d2d4 e5d4": ["f3d4"],
    "e2e4 e7e5 g1f3 b8c6 d2d4 e5d4 f3d4": ["f8c5", "g8f6"],
    "e2e4 e7e5 g1f3 b8c6 d2d4 e5d4 f3d4 f8c5": ["c1e3"],
    "e2e4 e7e5 g1f3 b8c6 d2d4 e5d4 f3d4 g8f6": ["d4c6"],
    
    # ───────────────────────────────────────────────────────────────
    # PETROV DEFENSE (Russian Game)
    # ───────────────────────────────────────────────────────────────
    "e2e4 e7e5 g1f3 g8f6": ["f3e5", "d2d4"],
    "e2e4 e7e5 g1f3 g8f6 f3e5": ["d7d6"],
    "e2e4 e7e5 g1f3 g8f6 f3e5 d7d6": ["e5f3"],
    "e2e4 e7e5 g1f3 g8f6 f3e5 d7d6 e5f3": ["f6e4"],
    
    # ═══════════════════════════════════════════════════════════════
    # SICILIAN DEFENSE - 10+ moves
    # ═══════════════════════════════════════════════════════════════
    "e2e4 c7c5": ["g1f3", "b1c3"],
    "e2e4 c7c5 g1f3": ["d7d6", "b8c6", "e7e6"],
    
    # Open Sicilian
    "e2e4 c7c5 g1f3 d7d6": ["d2d4"],
    "e2e4 c7c5 g1f3 d7d6 d2d4": ["c5d4"],
    "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4": ["f3d4"],
    "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4": ["g8f6"],
    "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6": ["b1c3"],
    "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3": ["a7a6", "g7g6"],
    
    # Najdorf Variation - DEEP LINE
    "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 a7a6": ["f1e2", "c1g5", "f2f3"],
    "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 a7a6 f1e2": ["e7e5"],
    "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 a7a6 f1e2 e7e5": ["d4b3"],
    "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 a7a6 f1e2 e7e5 d4b3": ["f8e7"],
    "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 a7a6 f1e2 e7e5 d4b3 f8e7": ["e1g1"],
    
    # Dragon Variation - DEEP LINE
    "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 g7g6": ["c1e3", "f2f3"],
    "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 g7g6 c1e3": ["f8g7"],
    "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 g7g6 c1e3 f8g7": ["f2f3"],
    "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 g7g6 c1e3 f8g7 f2f3": ["e8g8"],
    "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 g7g6 c1e3 f8g7 f2f3 e8g8": ["d1d2"],
    
    # Sveshnikov Variation
    "e2e4 c7c5 g1f3 b8c6": ["d2d4"],
    "e2e4 c7c5 g1f3 b8c6 d2d4": ["c5d4"],
    "e2e4 c7c5 g1f3 b8c6 d2d4 c5d4": ["f3d4"],
    "e2e4 c7c5 g1f3 b8c6 d2d4 c5d4 f3d4": ["g8f6"],
    "e2e4 c7c5 g1f3 b8c6 d2d4 c5d4 f3d4 g8f6": ["b1c3"],
    "e2e4 c7c5 g1f3 b8c6 d2d4 c5d4 f3d4 g8f6 b1c3": ["e7e5"],
    
    # ═══════════════════════════════════════════════════════════════
    # FRENCH DEFENSE - 10+ moves
    # ═══════════════════════════════════════════════════════════════
    "e2e4 e7e6": ["d2d4", "d2d3"],
    "e2e4 e7e6 d2d4": ["d7d5"],
    "e2e4 e7e6 d2d4 d7d5": ["b1c3", "e4d5", "e4e5"],
    
    # Winawer Variation - DEEP LINE
    "e2e4 e7e6 d2d4 d7d5 b1c3": ["f8b4"],
    "e2e4 e7e6 d2d4 d7d5 b1c3 f8b4": ["e4e5"],
    "e2e4 e7e6 d2d4 d7d5 b1c3 f8b4 e4e5": ["c7c5"],
    "e2e4 e7e6 d2d4 d7d5 b1c3 f8b4 e4e5 c7c5": ["a2a3"],
    "e2e4 e7e6 d2d4 d7d5 b1c3 f8b4 e4e5 c7c5 a2a3": ["b4c3"],
    "e2e4 e7e6 d2d4 d7d5 b1c3 f8b4 e4e5 c7c5 a2a3 b4c3": ["b2c3"],
    "e2e4 e7e6 d2d4 d7d5 b1c3 f8b4 e4e5 c7c5 a2a3 b4c3 b2c3": ["g8e7"],
    "e2e4 e7e6 d2d4 d7d5 b1c3 f8b4 e4e5 c7c5 a2a3 b4c3 b2c3 g8e7": ["d1g4"],
    
    # Classical Variation
    "e2e4 e7e6 d2d4 d7d5 b1c3 g8f6": ["c1g5"],
    "e2e4 e7e6 d2d4 d7d5 b1c3 g8f6 c1g5": ["f8e7"],
    "e2e4 e7e6 d2d4 d7d5 b1c3 g8f6 c1g5 f8e7": ["e4e5"],
    
    # Exchange Variation
    "e2e4 e7e6 d2d4 d7d5 e4d5": ["e6d5"],
    "e2e4 e7e6 d2d4 d7d5 e4d5 e6d5": ["b1c3"],
    
    # ═══════════════════════════════════════════════════════════════
    # CARO-KANN DEFENSE - 10+ moves
    # ═══════════════════════════════════════════════════════════════
    "e2e4 c7c6": ["d2d4", "b1c3"],
    "e2e4 c7c6 d2d4": ["d7d5"],
    "e2e4 c7c6 d2d4 d7d5": ["b1c3", "e4d5", "e4e5"],
    
    # Classical Variation - DEEP LINE
    "e2e4 c7c6 d2d4 d7d5 b1c3": ["d5e4"],
    "e2e4 c7c6 d2d4 d7d5 b1c3 d5e4": ["c3e4"],
    "e2e4 c7c6 d2d4 d7d5 b1c3 d5e4 c3e4": ["c8f5"],
    "e2e4 c7c6 d2d4 d7d5 b1c3 d5e4 c3e4 c8f5": ["e4g3"],
    "e2e4 c7c6 d2d4 d7d5 b1c3 d5e4 c3e4 c8f5 e4g3": ["f5g6"],
    "e2e4 c7c6 d2d4 d7d5 b1c3 d5e4 c3e4 c8f5 e4g3 f5g6": ["h2h4"],
    "e2e4 c7c6 d2d4 d7d5 b1c3 d5e4 c3e4 c8f5 e4g3 f5g6 h2h4": ["h7h6"],
    "e2e4 c7c6 d2d4 d7d5 b1c3 d5e4 c3e4 c8f5 e4g3 f5g6 h2h4 h7h6": ["g1f3"],
    
    # Advance Variation
    "e2e4 c7c6 d2d4 d7d5 e4e5": ["c8f5"],
    "e2e4 c7c6 d2d4 d7d5 e4e5 c8f5": ["b1c3"],
    "e2e4 c7c6 d2d4 d7d5 e4e5 c8f5 b1c3": ["e7e6"],
    
    # ═══════════════════════════════════════════════════════════════
    # PIRC DEFENSE
    # ═══════════════════════════════════════════════════════════════
    "e2e4 d7d6": ["d2d4"],
    "e2e4 d7d6 d2d4": ["g8f6"],
    "e2e4 d7d6 d2d4 g8f6": ["b1c3"],
    "e2e4 d7d6 d2d4 g8f6 b1c3": ["g7g6"],
    "e2e4 d7d6 d2d4 g8f6 b1c3 g7g6": ["f2f4"],
    
    # ═══════════════════════════════════════════════════════════════
    # ALEKHINE'S DEFENSE
    # ═══════════════════════════════════════════════════════════════
    "e2e4 g8f6": ["e4e5"],
    "e2e4 g8f6 e4e5": ["f6d5"],
    "e2e4 g8f6 e4e5 f6d5": ["d2d4"],
    "e2e4 g8f6 e4e5 f6d5 d2d4": ["d7d6"],
    
    # ═══════════════════════════════════════════════════════════════
    # 1.d4 OPENINGS
    # ═══════════════════════════════════════════════════════════════
    
    "d2d4": ["d7d5", "g8f6", "f7f5", "e7e6"],
    
    # ───────────────────────────────────────────────────────────────
    # QUEEN'S GAMBIT - 10+ moves
    # ───────────────────────────────────────────────────────────────
    "d2d4 d7d5": ["c2c4", "g1f3"],
    "d2d4 d7d5 c2c4": ["e7e6", "c7c6", "d5c4"],
    
    # Queen's Gambit Declined - DEEP LINE
    "d2d4 d7d5 c2c4 e7e6": ["b1c3", "g1f3"],
    "d2d4 d7d5 c2c4 e7e6 b1c3": ["g8f6"],
    "d2d4 d7d5 c2c4 e7e6 b1c3 g8f6": ["c1g5"],
    "d2d4 d7d5 c2c4 e7e6 b1c3 g8f6 c1g5": ["f8e7"],
    "d2d4 d7d5 c2c4 e7e6 b1c3 g8f6 c1g5 f8e7": ["e2e3"],
    "d2d4 d7d5 c2c4 e7e6 b1c3 g8f6 c1g5 f8e7 e2e3": ["e8g8"],
    "d2d4 d7d5 c2c4 e7e6 b1c3 g8f6 c1g5 f8e7 e2e3 e8g8": ["g1f3"],
    "d2d4 d7d5 c2c4 e7e6 b1c3 g8f6 c1g5 f8e7 e2e3 e8g8 g1f3": ["b8d7"],
    "d2d4 d7d5 c2c4 e7e6 b1c3 g8f6 c1g5 f8e7 e2e3 e8g8 g1f3 b8d7": ["a1c1"],
    "d2d4 d7d5 c2c4 e7e6 b1c3 g8f6 c1g5 f8e7 e2e3 e8g8 g1f3 b8d7 a1c1": ["c7c6"],
    
    # Slav Defense - DEEP LINE
    "d2d4 d7d5 c2c4 c7c6": ["g1f3", "b1c3"],
    "d2d4 d7d5 c2c4 c7c6 g1f3": ["g8f6"],
    "d2d4 d7d5 c2c4 c7c6 g1f3 g8f6": ["b1c3"],
    "d2d4 d7d5 c2c4 c7c6 g1f3 g8f6 b1c3": ["d5c4"],
    "d2d4 d7d5 c2c4 c7c6 g1f3 g8f6 b1c3 d5c4": ["a2a4"],
    "d2d4 d7d5 c2c4 c7c6 g1f3 g8f6 b1c3 d5c4 a2a4": ["c8f5"],
    "d2d4 d7d5 c2c4 c7c6 g1f3 g8f6 b1c3 d5c4 a2a4 c8f5": ["e2e3"],
    "d2d4 d7d5 c2c4 c7c6 g1f3 g8f6 b1c3 d5c4 a2a4 c8f5 e2e3": ["e7e6"],
    
    # Queen's Gambit Accepted
    "d2d4 d7d5 c2c4 d5c4": ["g1f3"],
    "d2d4 d7d5 c2c4 d5c4 g1f3": ["g8f6"],
    "d2d4 d7d5 c2c4 d5c4 g1f3 g8f6": ["e2e3"],
    
    # ───────────────────────────────────────────────────────────────
    # KING'S INDIAN DEFENSE - 10+ moves
    # ───────────────────────────────────────────────────────────────
    "d2d4 g8f6": ["c2c4", "g1f3"],
    "d2d4 g8f6 c2c4": ["g7g6", "e7e6"],
    "d2d4 g8f6 c2c4 g7g6": ["b1c3", "g2g3"],
    "d2d4 g8f6 c2c4 g7g6 b1c3": ["f8g7"],
    "d2d4 g8f6 c2c4 g7g6 b1c3 f8g7": ["e2e4"],
    "d2d4 g8f6 c2c4 g7g6 b1c3 f8g7 e2e4": ["d7d6"],
    "d2d4 g8f6 c2c4 g7g6 b1c3 f8g7 e2e4 d7d6": ["g1f3"],
    "d2d4 g8f6 c2c4 g7g6 b1c3 f8g7 e2e4 d7d6 g1f3": ["e8g8"],
    "d2d4 g8f6 c2c4 g7g6 b1c3 f8g7 e2e4 d7d6 g1f3 e8g8": ["f1e2"],
    "d2d4 g8f6 c2c4 g7g6 b1c3 f8g7 e2e4 d7d6 g1f3 e8g8 f1e2": ["e7e5"],
    "d2d4 g8f6 c2c4 g7g6 b1c3 f8g7 e2e4 d7d6 g1f3 e8g8 f1e2 e7e5": ["e1g1"],
    "d2d4 g8f6 c2c4 g7g6 b1c3 f8g7 e2e4 d7d6 g1f3 e8g8 f1e2 e7e5 e1g1": ["b8c6"],
    
    # ───────────────────────────────────────────────────────────────
    # NIMZO-INDIAN DEFENSE - 10+ moves
    # ───────────────────────────────────────────────────────────────
    "d2d4 g8f6 c2c4 e7e6": ["b1c3"],
    "d2d4 g8f6 c2c4 e7e6 b1c3": ["f8b4"],
    "d2d4 g8f6 c2c4 e7e6 b1c3 f8b4": ["e2e3", "d1c2"],
    "d2d4 g8f6 c2c4 e7e6 b1c3 f8b4 e2e3": ["e8g8"],
    "d2d4 g8f6 c2c4 e7e6 b1c3 f8b4 e2e3 e8g8": ["f1d3"],
    "d2d4 g8f6 c2c4 e7e6 b1c3 f8b4 e2e3 e8g8 f1d3": ["d7d5"],
    "d2d4 g8f6 c2c4 e7e6 b1c3 f8b4 e2e3 e8g8 f1d3 d7d5": ["g1f3"],
    
    # ───────────────────────────────────────────────────────────────
    # QUEEN'S INDIAN DEFENSE
    # ───────────────────────────────────────────────────────────────
    "d2d4 g8f6 c2c4 e7e6 g1f3": ["b7b6"],
    "d2d4 g8f6 c2c4 e7e6 g1f3 b7b6": ["g2g3"],
    "d2d4 g8f6 c2c4 e7e6 g1f3 b7b6 g2g3": ["c8b7"],
    
    # ───────────────────────────────────────────────────────────────
    # DUTCH DEFENSE - 10+ moves
    # ───────────────────────────────────────────────────────────════
    "d2d4 f7f5": ["g2g3", "c2c4"],
    "d2d4 f7f5 g2g3": ["g8f6"],
    "d2d4 f7f5 g2g3 g8f6": ["f1g2"],
    "d2d4 f7f5 g2g3 g8f6 f1g2": ["e7e6"],
    "d2d4 f7f5 g2g3 g8f6 f1g2 e7e6": ["g1f3"],
    "d2d4 f7f5 g2g3 g8f6 f1g2 e7e6 g1f3": ["f8e7"],
    "d2d4 f7f5 g2g3 g8f6 f1g2 e7e6 g1f3 f8e7": ["e1g1"],
    "d2d4 f7f5 g2g3 g8f6 f1g2 e7e6 g1f3 f8e7 e1g1": ["e8g8"],
    
    # ───────────────────────────────────────────────────────────────
    # LONDON SYSTEM (White's setup)
    # ───────────────────────────────────────────────────────────────
    "d2d4 g8f6 g1f3": ["e7e6", "d7d5"],
    "d2d4 d7d5 g1f3": ["g8f6"],
    "d2d4 d7d5 g1f3 g8f6": ["c1f4"],
    "d2d4 d7d5 g1f3 g8f6 c1f4": ["e7e6"],
    "d2d4 d7d5 g1f3 g8f6 c1f4 e7e6": ["e2e3"],
    
    # ═══════════════════════════════════════════════════════════════
    # 1.c4 ENGLISH OPENING - 10+ moves
    # ═══════════════════════════════════════════════════════════════
    "c2c4": ["e7e5", "g8f6", "c7c5"],
    "c2c4 e7e5": ["b1c3", "g2g3"],
    "c2c4 e7e5 b1c3": ["g8f6"],
    "c2c4 e7e5 b1c3 g8f6": ["g1f3"],
    "c2c4 e7e5 b1c3 g8f6 g1f3": ["b8c6"],
    "c2c4 e7e5 b1c3 g8f6 g1f3 b8c6": ["g2g3"],
    "c2c4 e7e5 b1c3 g8f6 g1f3 b8c6 g2g3": ["f8b4"],
    "c2c4 e7e5 b1c3 g8f6 g1f3 b8c6 g2g3 f8b4": ["f1g2"],
    
    "c2c4 g8f6": ["b1c3", "g2g3"],
    "c2c4 g8f6 b1c3": ["e7e5"],
    "c2c4 g8f6 g2g3": ["g7g6"],
    "c2c4 g8f6 g2g3 g7g6": ["f1g2"],
    "c2c4 g8f6 g2g3 g7g6 f1g2": ["f8g7"],
    
    # Symmetrical English
    "c2c4 c7c5": ["g1f3", "b1c3"],
    "c2c4 c7c5 g1f3": ["g8f6"],
    "c2c4 c7c5 b1c3": ["b8c6"],
    
    # ═══════════════════════════════════════════════════════════════
    # 1.Nf3 RETI OPENING
    # ═══════════════════════════════════════════════════════════════
    "g1f3": ["d7d5", "g8f6"],
    "g1f3 d7d5": ["c2c4"],
    "g1f3 d7d5 c2c4": ["d5c4"],
    "g1f3 g8f6": ["c2c4"],
    
    # ═══════════════════════════════════════════════════════════════
    # TACTICAL TRAPS & GAMBITS
    # ═══════════════════════════════════════════════════════════════
    
    # ───────────────────────────────────────────────────────────────
    # STAFFORD GAMBIT (Trap for Black against e4 e5 Nf3 Nf6)
    # ───────────────────────────────────────────────────────────────
    # If white takes e5, black plays Nc6 and sets trap
    "e2e4 e7e5 g1f3 g8f6 f3e5": ["b8c6"],
    "e2e4 e7e5 g1f3 g8f6 f3e5 b8c6": ["e5c6"],  # White falls into trap
    "e2e4 e7e5 g1f3 g8f6 f3e5 b8c6 e5c6": ["d7c6"],  # Black gets initiative
    
    # ───────────────────────────────────────────────────────────────
    # ELEPHANT GAMBIT (Trap)
    # ───────────────────────────────────────────────────────────────
    "e2e4 e7e5 g1f3 e5e4": ["f3g5"],  # White should play this
    
    # ───────────────────────────────────────────────────────────────
    # FISHING POLE TRAP (In Ruy Lopez)
    # ───────────────────────────────────────────────────────────────
    "e2e4 e7e5 g1f3 b8c6 f1b5 g8f6 e1g1 f6g4": ["h2h3"],  # White falls for trap
    
    # ───────────────────────────────────────────────────────────────
    # FRIED LIVER ATTACK (Aggressive Italian)
    # ───────────────────────────────────────────────────────────────
    "e2e4 e7e5 g1f3 b8c6 f1c4 g8f6 f3g5": ["d7d5"],
    "e2e4 e7e5 g1f3 b8c6 f1c4 g8f6 f3g5 d7d5": ["e4d5"],
    "e2e4 e7e5 g1f3 b8c6 f1c4 g8f6 f3g5 d7d5 e4d5": ["f6d5"],
    "e2e4 e7e5 g1f3 b8c6 f1c4 g8f6 f3g5 d7d5 e4d5 f6d5": ["g5f7"],  # Fried Liver!
    
    # ───────────────────────────────────────────────────────────────
    # LEGAL'S MATE TRAP
    # ───────────────────────────────────────────────────────────────
    "e2e4 e7e5 g1f3 d7d6 f1c4 c8g4": ["b1c3"],
    "e2e4 e7e5 g1f3 d7d6 f1c4 c8g4 b1c3": ["g7g6"],
    "e2e4 e7e5 g1f3 d7d6 f1c4 c8g4 b1c3 g7g6": ["f3e5"],  # Sacrifice!
    
    # ───────────────────────────────────────────────────────────────
    # BLACKBURNE SHILLING GAMBIT (Trap)
    # ───────────────────────────────────────────────────────────────
    "e2e4 e7e5 g1f3 b8c6 f1c4 f6d4": ["f3e5"],  # White falls for trap
}

# ═══════════════════════════════════════════════════════════════
# HASH-BASED OPENING BOOK (PERFORMANCE OPTIMIZATION)
# ═══════════════════════════════════════════════════════════════

# Global variable - built on first access
_OPENING_BOOK_HASHED = None

def _hash_sequence(moves_str):
    """Convert 'e2e4 e7e5' to a Zobrist hash integer"""
    # Import here to avoid circular dependency
    import ChessEngine
    
    gs = ChessEngine.GameState()
    if not moves_str:  # Empty string = starting position
        return gs.zobristHash
    
    for move_str in moves_str.split():
        valid_moves = gs.getValidMoves()
        for m in valid_moves:
            if m.getChessNotation() == move_str:
                gs.makeMove(m)
                break
    
    return gs.zobristHash


def get_opening_book_hashed():
    """
    Lazy initialization of hash-based opening book.
    Builds on first call to avoid circular import.
    """
    global _OPENING_BOOK_HASHED
    
    if _OPENING_BOOK_HASHED is None:
        print("🔨 Building hash-based opening book...")
        _OPENING_BOOK_HASHED = {}
        for key, value in OPENING_BOOK.items():
            hash_key = _hash_sequence(key)
            _OPENING_BOOK_HASHED[hash_key] = value
        print(f"✅ Opening book ready: {len(_OPENING_BOOK_HASHED)} positions")
    
    return _OPENING_BOOK_HASHED
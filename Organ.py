# ------------------------------------------------------------
# Organ.mid – Church Organ Pad Track (Powerwolf style)
# 외부 라이브러리 없이 순수 Python MIDI 생성
# ------------------------------------------------------------

def write_varlen(value):
    out = [value & 0x7F]
    value >>= 7
    while value:
        out.insert(0, (value & 0x7F) | 0x80)
        value >>= 7
    return bytes(out)

def create_midi_organ(filename="Organ.mid"):
    tempo = 60000000 // 180  # BPM 180
    tpq = 480
    measure = tpq * 4        # 4 beats per measure

    # Church Organ chords (D minor progression)
    chords = [
        [62, 65, 69],  # Dm (D4, F4, A4)
        [58, 62, 65],  # Bb (Bb3, D4, F4)
        [60, 64, 67],  # C (C4, E4, G4)
        [65, 69, 72],  # F (F4, A4, C5)
        [69, 72, 76]   # A (A4, C5, E5)
    ]

    # Header
    header = (
        b"MThd" +
        (6).to_bytes(4, "big") +
        (0).to_bytes(2, "big") +
        (1).to_bytes(2, "big") +
        tpq.to_bytes(2, "big")
    )

    # Track
    track = bytearray()

    # Tempo
    track += b"\x00\xFF\x51\x03" + tempo.to_bytes(3, "big")

    # Program change – Church Organ (19)
    track += b"\x00" + bytes([0xC0, 19])

    # Write 64 measures
    for i in range(64):
        chord = chords[i % len(chords)]

        # note_on for each note in chord
        for note in chord:
            track += write_varlen(0)
            track += bytes([0x90, note, 80])

        # sustain for 1 measure
        track += write_varlen(measure)

        # note_off
        for note in chord:
            track += bytes([0x80, note, 40])

    # End track
    track += b"\x00\xFF\x2F\x00"

    # Track chunk
    chunk = b"MTrk" + len(track).to_bytes(4, "big") + track

    with open(filename, "wb") as f:
        f.write(header + chunk)

    print("🎹 Organ.mid 생성 완료")

# RUN
create_midi_organ()

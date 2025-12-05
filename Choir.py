# ------------------------------------------------------------
# Choir.mid – Choir Aahs 패드, 하드록 후렴 보강용
# 외부 라이브러리 없이 순수 Python MIDI 생성
# ------------------------------------------------------------

def write_varlen(value):
    out = [value & 0x7F]
    value >>= 7
    while value:
        out.insert(0, (value & 0x7F) | 0x80)
        value >>= 7
    return bytes(out)

def create_midi_choir(filename="Choir.mid"):
    tempo = 60000000 // 180  # BPM 180
    tpq = 480
    sustain = tpq * 3        # 3 beats hold
    rest = tpq * 1           # 1 beat rest

    # Choir chords (high pad)
    chords = [
        [74, 77, 81],   # Dm (D5, F5, A5)
        [70, 74, 77],   # Bb
        [72, 76, 79],   # C
        [77, 81, 84],   # F
        [81, 84, 88]    # A
    ]

    # Header
    header = (
        b"MThd" +
        (6).to_bytes(4, "big") +
        (0).to_bytes(2, "big") +
        (1).to_bytes(2, "big") +
        tpq.to_bytes(2, "big")
    )

    track = bytearray()

    # Tempo
    track += b"\x00\xFF\x51\x03" + tempo.to_bytes(3, "big")

    # Program change – Choir Aahs (52)
    track += b"\x00" + bytes([0xC0, 52])

    for i in range(64):
        chord = chords[i % len(chords)]

        # note_on all
        for note in chord:
            track += write_varlen(0)
            track += bytes([0x90, note, 70])  # lighter velocity

        # sustain 3 beats
        track += write_varlen(sustain)

        # note_off
        for note in chord:
            track += bytes([0x80, note, 40])

        # rest 1 beat
        track += write_varlen(rest)

    # End track
    track += b"\x00\xFF\x2F\x00"

    chunk = b"MTrk" + len(track).to_bytes(4, "big") + track

    with open(filename, "wb") as f:
        f.write(header + chunk)

    print("🎶 Choir.mid 생성 완료")

# RUN
create_midi_choir()

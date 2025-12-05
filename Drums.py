# ------------------------------------------------------------
# Drums.mid – 180BPM Hard Rock / Power Metal Drum Track
# 외부 라이브러리 없이 순수 Python MIDI 생성
# ------------------------------------------------------------

def write_varlen(value):
    out = [value & 0x7F]
    value >>= 7
    while value:
        out.insert(0, (value & 0x7F) | 0x80)
        value >>= 7
    return bytes(out)

def create_midi_drums(filename="Drums.mid"):
    tempo = 60000000 // 180  # BPM 180
    tpq = 480
    sixteenth = tpq // 4      # Kick pattern
    eighth = tpq // 2         # Hi-hat
    quarter = tpq             # Snare

    # --- Drum MIDI note numbers ---
    KICK = 36
    SNARE = 38
    HAT = 42        # Closed Hi Hat
    CRASH = 49

    # --- Header ---
    header = (
        b"MThd" +
        (6).to_bytes(4, "big") +
        (0).to_bytes(2, "big") +  # format 0
        (1).to_bytes(2, "big") +  # single track
        tpq.to_bytes(2, "big")
    )

    # --- Track ---
    track = bytearray()

    # Tempo
    track += b"\x00\xFF\x51\x03" + tempo.to_bytes(3, "big")

    # Channel 10 uses status 0x99 for note_on, 0x89 for note_off

    for bar in range(64):  # 64 measures
        # Crash on first beat
        track += write_varlen(0)
        track += bytes([0x99, CRASH, 110])
        track += write_varlen(quarter)
        track += bytes([0x89, CRASH, 64])

        # 4 beats per bar
        for beat in range(4):
            # Snare on beats 1 and 3 (2 and 4 by human count)
            if beat in [1, 3]:
                track += write_varlen(0)
                track += bytes([0x99, SNARE, 120])
                track += write_varlen(0)
                track += bytes([0x89, SNARE, 60])

            # Hi-hat 8th notes
            for hh in range(2):
                track += write_varlen(0)
                track += bytes([0x99, HAT, 80])
                track += write_varlen(eighth)
                track += bytes([0x89, HAT, 40])

            # Kick 16th pattern (4 notes per beat)
            for k in range(4):
                track += write_varlen(0)
                track += bytes([0x99, KICK, 100])
                track += write_varlen(sixteenth)
                track += bytes([0x89, KICK, 50])

    # End of track
    track += b"\x00\xFF\x2F\x00"

    # Track chunk
    chunk = b"MTrk" + len(track).to_bytes(4, "big") + track

    with open(filename, "wb") as f:
        f.write(header + chunk)

    print("🥁 Drums.mid 생성 완료")

# RUN
create_midi_drums()

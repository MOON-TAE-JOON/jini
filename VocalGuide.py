# ------------------------------------------------------------
# VocalGuide.mid – 보컬 멜로디 가이드 트랙
# 외부 라이브러리 없이 순수 Python MIDI 생성
# ------------------------------------------------------------

def write_varlen(value):
    out = [value & 0x7F]
    value >>= 7
    while value:
        out.insert(0, (value & 0x7F) | 0x80)
        value >>= 7
    return bytes(out)

def create_midi_vocal(filename="VocalGuide.mid"):
    tempo = 60000000 // 180  # BPM 180
    tpq = 480
    duration = tpq           # 1 beat note

    # Vocal patch – Lead Voice (85)
    PATCH = 85

    # Section melodic patterns
    verse_pattern = [62, 65, 67, 69]     # D4 F4 G4 A4
    pre_pattern   = [69, 72]             # A4 C5
    chorus_pattern = [74, 77, 81, 84, 86] # D5 F5 A5 C6 D6

    # Build full 64-bar melody (simplified)
    full_melody = []
    for bar in range(64):
        if bar % 20 < 8:    # first 8 bars → verse
            full_melody.append(verse_pattern[bar % len(verse_pattern)])
        elif bar % 20 < 12: # next 4 bars → pre-chorus
            full_melody.append(pre_pattern[bar % len(pre_pattern)])
        else:               # last 8 bars → chorus
            full_melody.append(chorus_pattern[bar % len(chorus_pattern)])

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

    # Program change – Lead Voice (85)
    track += b"\x00" + bytes([0xC0, PATCH])

    # Note events
    for note in full_melody:
        # note_on
        track += write_varlen(0)
        track += bytes([0x90, note, 100])

        # note_off after 1 beat
        track += write_varlen(duration)
        track += bytes([0x80, note, 60])

    # End of track
    track += b"\x00\xFF\x2F\x00"

    # Save
    chunk = b"MTrk" + len(track).to_bytes(4, "big") + track
    with open(filename, "wb") as f:
        f.write(header + chunk)

    print("🎤 VocalGuide.mid 생성 완료")

# RUN
create_midi_vocal()

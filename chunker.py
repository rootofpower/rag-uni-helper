def load_and_chunk(filepath, chunk_size=3):
    with open(filepath, 'rt') as f:
        text = f.read()
        text = text.replace("\n", " ")

    sentences = text.split(". ")

    chunks = []
    for i in range(0, len(sentences), chunk_size):
        chunk = ". ".join(sentences[i:i + chunk_size])
        chunks.append(chunk)

    return chunks

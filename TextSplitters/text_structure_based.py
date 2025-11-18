from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import CharacterTextSplitter

text = """Poetry is one of the oldest and most expressive forms of human communication. It uses rhythm, imagery, and carefully chosen words to convey emotions, experiences, and ideas in a way that ordinary language often cannot. Unlike prose, poetry is not bound by strict rules of sentence structure or narrative flow. Instead, it allows the writer to experiment with form, sound, and meaning, creating a unique space where language becomes more than a tool for information—it becomes art.

At its heart, poetry captures the essence of human feelings. A poem can express joy, sorrow, confusion, hope, or longing in just a few lines. Through metaphors and symbols, poets transform ordinary objects or moments into something deeper. For example, a falling leaf may represent loss, or a sunrise may symbolize new beginnings. These layers of meaning encourage readers to engage with the poem in a personal way, finding their own interpretations within the lines.

Poetry also plays an important cultural role. Across history, poems have been used to preserve myths, celebrate heroes, challenge social norms, and share spiritual beliefs. From ancient epics to modern spoken-word performances, poetry has helped shape the identity of communities and nations. It has given people a voice during times of struggle and a way to celebrate moments of triumph.

Another defining feature of poetry is its musical quality. Sound devices like rhyme, alliteration, and rhythm create patterns that make poems memorable and enjoyable to read aloud. Even free verse, which does not follow a specific meter or rhyme scheme, often relies on the natural rhythm of language to create emotional impact.

Ultimately, poetry invites us to slow down and observe the world with greater attention. It encourages reflection, imagination, and empathy. Whether simple or complex, poetry remains a powerful reminder that language can touch the heart as much as it informs the mind.
"""

splitter =  RecursiveCharacterTextSplitter(
    chunk_size=100, 
    chunk_overlap=0
)

result = splitter.split_text(text)
print(result)
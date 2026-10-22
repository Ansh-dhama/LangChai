from langchain_text_splitters import CharacterTextSplitter


text ="""
Space Exploration is the use of astronomy and space technology to explore outer space. While astronomers use telescopes
 to explore space, both uncrewed robotic space missions and human spaceflight are used to explore it physically. 
One of the primary sources for space science is space exploration, which is similar 
to astronomy in its classical form.

We can use space exploration to validate or disprove scientific theories that
 have been created on Earth. Insights into gravity, the magnetosphere, the atmosphere
 , fluid dynamics, and the geological evolution of other planets have all come from
   studying the solar system.
"""

splitter = CharacterTextSplitter(
    chunk_size =100,
    chunk_overlap = 0,
    separator =''
)

print(splitter.split_text(text))














































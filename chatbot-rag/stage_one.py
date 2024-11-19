import streamlit as st

def run_stage_one(msg, vectorstore, llm, system_prompt, query, prompt):
    with st.chat_message("ai"):
        with st.status(msg):
            retriever = vectorstore.as_retriever(search_kwargs={'k': 3})
            ctx = '\n\n'.join(c.page_content for c in retriever.invoke(query))
            st.write(f"Found a context with {len(ctx)} characters.")
            st.write(ctx)
            st.write(f"Found using the query: {query}")

            completion = llm.chat.completions.create(
                messages=system_prompt + [{"role": "system", "content": f"Context: {ctx[0:100]}"}] + [
                    {"role": "user", "content": prompt}
                ],
                model="", stream=True, max_tokens=1000
            )
            response_placeholder = st.empty()  # Placeholder for the streamed response
            response = ""
            for chunk in completion:
                if not chunk.choices[0].finish_reason:
                    delta_content = chunk.choices[0].delta.content
                    response += delta_content
                    response_placeholder.write(response)  # Update the placeholder with the streamed content

            st.session_state.contexts.extend([
                {"role": "system", "content": f"Context: {response}"},
            ])

def run_stage_two(msg, llm, system_prompt, prompt):
    with st.chat_message("ai"):
        with st.status(msg):
            completion = llm.chat.completions.create(
                messages=system_prompt + st.session_state.contexts + [
                    {"role": "user", "content": prompt}
                ],
                model="", stream=True, max_tokens=1000
            )
            response_placeholder = st.empty()  # Placeholder for the streamed response
            response = ""
            for chunk in completion:
                if not chunk.choices[0].finish_reason:
                    delta_content = chunk.choices[0].delta.content
                    response += delta_content
                    response_placeholder.write(response)  # Update the placeholder with the streamed content

            st.session_state.messages.extend([
                {"role": "ai", "content": response},
            ])

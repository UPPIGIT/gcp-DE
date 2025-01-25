## LLMs

Hello everyone and welcome back.

**Let's talk about large language models, also known as LLMs. So what is an LLM and why are we hearing so much about it?**

Just to help you understand in a very easy way, at a very high level, when we are on a smartphone trying to text somebody and there is a predictive text feature that comes in there. So like you can see the person types in "cant" and the system predicts the next words as "wait," "believe," or "remember." That's pretty much what an LLM is at a very high level. But of course, it's much more massive.

There is a lot more accuracy and there are a lot of other components also involved. Likewise, when we type something in ChatGPT and it answers for us, that is also an LLM, a very strong one.

So yes, ChatGPT is also an LLM. LLMs are nothing but a specific type of AI models that are designed to understand and generate human-like text. So there is only one key takeaway that you need to remember from this slide: LLM means text.

They can understand text, they can process text, they can generate text.

They know about words, grammar, sentences, context, all of this with great accuracy.

Now people often use the words "generative AI" and "LLM" interchangeably, but that is not correct.

Generative AI is a broader term and it can mean generation of text, image, audio, video, code, anything. On the other hand, LLM deals only with text.

So anytime we are talking about generative AI but only for generating text, think about LLMs.

## Now how does an LLM work?

We already know about neural networks and their capability to handle complex scenarios effectively due to their layered structure. So the brains behind the LLM is a specific type of neural network, also called transformers. We will not go into depth of what a transformer is, but the only key thing to know is the way that they are architected. They can understand language, they can understand meaning, they can understand context, all of that.

And we will see this in more detail when we are talking about embeddings later.

But for now, just remember that transformers are a type of neural network that's really good at understanding human language—words, meaning, context, etc.

And this transformer is trained on lots of training data, in fact, much more than what we see. For example, ChatGPT is trained on the entire Wikipedia and many more text-based websites, blogs, manuals, etc.

Based on this learning, it is really good at understanding text and delivering the output. So when you ask ChatGPT something, it uses this training and learning to generate your output. 

And last, a very important thing to note here is when we say output, it really means one word at a time.

When we use ChatGPT and when we see it giving out long sentences or paragraphs, in reality, it is predicting only one word, just one word at a time, the next word at a time. And it is doing it again and again, resulting in the long sentences and paragraphs that you see. So this is a very basic understanding of how LLMs work.

## A few key things that you need to know about LLMs

First is their training.

When we were in the last module, I asked you to remember three key takeaways.

The first one of them was: training a model on a good amount of data is very important for it to be effective.

Large language models are trained on huge corpora of data. That's what the word large in LLM means.

For example, if I talk about OpenAI or ChatGPT, they do not disclose the real volume of data that was used to train it. But some sources say that GPT-3, which is an older version of what we see today, was trained on around 500+ GB of text data, which is an enormous volume. This big dataset means that it has seen different kinds of words, grammar, sentences, semantics, facts, information, everything. And when you feed this volume of data, obviously the model will be able to train better and answer questions more accurately.

Second is size and scale.

LLMs use massive neural networks that are called transformers, like I mentioned, and they contain billions of parameters. You can think of parameters like a knowledge bank, like a variable that is used to train the model during training. So the higher the number of parameters, the better the model’s training, understanding, and generation capability. Now again, GPT-3, which was an older version of the 3.5 or 4 that we are using today, was trained on 175 billion parameters. Palm, which is an LLM from Google, has 540 billion parameters.

Just imagine. That's why if you look at ChatGPT, for example, you ask it anything, it understands your question, it gives a good answer. And the reason for that is its training on a massive dataset, like I mentioned, and this huge number of parameters-based transformer neural network.

Third and last point: the training does not stop here.

What we saw in here was our pre-training that the models come already done with. Then we can also have some fine-tuning, meaning we can further tune the LLM towards a more specific and task-oriented dataset. We will talk about fine-tuning in more depth later.

But just to give you an example, if we want to use an LLM for text completion or summarization, we can fine-tune it by exposing it to data related to these tasks. 

For example, I want my LLM to answer data-related questions related to healthcare, so I can train it on a healthcare-related dataset. It will make sure that the LLM is more suited to your task, and it is better at generating content for that domain or task.

## Okay, so where can LLMs be used?

Answer: anywhere that involves text, and in fact, they are being used in many of these spaces already.

### 1. Content Generation
So if you are in marketing, advertising, sales, or anywhere else, we can use LLMs like ChatGPT or Lama for our text content generation.

### 2. Chatbot
This is one area where LLMs will make a huge impact. When we are chatting with customer support, LLMs can replace that first level of engagement and answer questions for you based on the company's documentation. And if the user is still not satisfied, they can go ahead and talk to a human.

So imagine how much effort you can save in the first place.

### 3. Language Translation
There are translators already available in the market for a long time, but LLMs can expand on those translations and do conversation-based chatting that can give you better results.

### 4. Text Summarization
Imagine you have a long thesis, legal contract, or project documentation. You don't need to read all of it. LLMs can generate the summary of that data for you.

In fact, guys, I have personally created an application for it. You can ask it for long summaries, short summaries, or executive-level summaries. It can give you all of that with amazing details and accuracy.

### 5. Q&A
Probably the most used use case. We ask ChatGPT any question and it gives us a pointed answer. Imagine if I want to know who won the Superbowl 2020. I do not have to go into Wikipedia and read a long document. I can just ask that question and get a pointed answer.

In the practical learning part of this course, later we will actually be creating a chatbot just like this, and then you will see it really in action.

So guys, these were some of the use cases of LLMs. But remember that the list does not end here. LLMs will change every way that we interact and manipulate text data. And the list of LLMs is growing every day—from GPT to Lama to Palm to pointed LLMs for the auto industry, finance industry, and more.

Every day, a new model is coming, and for sure we will get more and more innovative applications in the coming days.

Now that you understand what an LLM is and what their capabilities are, you will be ready to use them in your daily life and make your work smarter. 

Okay, so that was all about LLMs. Let's move on and check out another topic in the next video.


Here are some common use cases for Large Language Models (LLMs) like ChatGPT, GPT-4, and similar models:

### 1. **Customer Support Automation**
   - **Use Case:** Automate responses to customer inquiries in chat or email.
   - **Example:** AI-powered chatbots for handling FAQs, complaints, or tracking order issues.

---

### 2. **Content Generation**
   - **Use Case:** Generate articles, blogs, social media posts, or creative writing.
   - **Example:** Marketing copy for ad campaigns or SEO-optimized blog posts.

---

### 3. **Code Assistance**
   - **Use Case:** Help developers with code completion, debugging, or generating boilerplate code.
   - **Example:** Write Airflow DAGs, SQL queries, or Java Spring Boot microservices.

---

### 4. **Data Extraction & Transformation**
   - **Use Case:** Extract structured data from unstructured text, e.g., invoices or medical reports.
   - **Example:** Parsing healthcare claims data to extract provider and member information.

---

### 5. **Language Translation**
   - **Use Case:** Translate documents, websites, or applications in real time.
   - **Example:** Translating medical records from Spanish to English while retaining context.

---

### 6. **Summarization**
   - **Use Case:** Summarize lengthy documents, reports, or meeting notes.
   - **Example:** Executive summaries for legal documents or project updates.

---

### 7. **Search and Knowledge Retrieval**
   - **Use Case:** Enhance search functionality with natural language queries.
   - **Example:** Search a document repository with complex queries like “find contracts expiring in 2025.”

---

### 8. **Education and Training**
   - **Use Case:** Create personalized learning experiences or explain concepts.
   - **Example:** AI tutors explaining complex concepts like pharmacy networks or microservices.

---

### 9. **Healthcare Applications**
   - **Use Case:** Simplify medical data or generate insights from clinical notes.
   - **Example:** Automating data harmonization for patient records using GCP Healthcare APIs.

---

### 10. **Personalized Recommendations**
   - **Use Case:** Provide tailored suggestions for products, services, or content.
   - **Example:** Suggesting courses to upskill based on user interest or performance.

---

### 11. **Compliance and Auditing**
   - **Use Case:** Assist in document review, flagging inconsistencies or violations.
   - **Example:** Validating firewall rules or ensuring compliance in geocoding processes.

---

### 12. **Conversation Simulation**
   - **Use Case:** Role-play scenarios for practice in interviews or customer interactions.
   - **Example:** Mock interviews for GCP-related roles or healthcare domain questions.

Do you have a specific use case in mind you'd like to explore?


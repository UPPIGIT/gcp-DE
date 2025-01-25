## LLMs

Hello everyone and welcome back.

**Let's talk about large language models, also known as LLM.So what is an LLM and why we are hearing so much about it?
Just to help you understand in a very easy way, at a very high level, when we are on a smartphone trying to text somebody and there is a predictive text feature that comes in there.So like you can see the person types in cant and the system predicts the next words as wait, believe or remember.That's pretty much what an is at a very high level.But of course it's more massive.**

**There is a lot of more accuracy and there are a lot of other components also involved.Likewise, when we type something in chat, GPT and it answers for us, that is also a LM, a very strong one.**

**So yes, chat GPT is also a LLM, so LMM are nothing but a specific type of AI models that are designed to understand and generate human like text.So there is only one key takeaway that you need to remember from this slide.And that is LLM means text.**

**They can understand text, they can process text, they can generate text**.

**They know about words, grammar, sentences, context, all of this with great accuracy.**

**Now people often use the words generative AI and interchangeably, but that is not correct.**

**Generative AI is a broader term and it can mean generation of text, image, audio, video, code.Anything, on the other hand, LLM deals only with text.**

**So anytime we are talking about generative AI but only for generating text, think about LMS.**

## Now how does a LM work?

**We already know about neural networks and their capability to handle complex scenarios effectively due
to their layered structure.So the brains behind the LLM is a specific type of neural network, also called as transformers.And we will not go into depth of what a transformer is.But the only key thing to know is the way that they are architectured they can understand language,they can understand meaning, they can understand context.All of that.**

And we will see this in more detail when we are talking about embeddings later.

**But for now, just remember that transformers is a type of neural network that's really good at understanding human language.Words are meaning, context, etcetera.**

**And this transformer is trained on lots of training data, in fact, much, much more than what we see.For example, ChatGPT is trained on entire Wikipedia and many more text based websites, blogs, manuals,etcetera.**

**And basis of this learning.It is really good at understanding text and delivering the output.So when you ask ChatGPT something, it uses this training and learning to generate you the output.And last very important thing to note in here is when we say output here, it really means one word at a time.**

**When we use ChatGPT and when we see it giving out long sentences paragraphs.In reality it is predicting only one word, just one word at a time, the next word at a time.And it is doing it again and again, resulting in the long sentences and paragraphs that you see.So this is a very basic understanding of how llms work.**

## Now, a few key things that you need to know about Llms first is their training.

**So when we were in the last module, I asked you to remember three key takeaways.**

**And the first one of it was training of a model on good amount of data is very important for it to be effective.**

**And large language models are trained on huge corpus of data.That's what the word large in LLM means.**

**For example, if I talk about OpenAI or ChatGPT, they do not disclose the real volume of data that was used to train it.But some sources say that GPT three, which is an older version of what we see today, was trained on around 500 plus GB of text data, which is enormous volume.This big dataset means that it has seen different kinds of words grammar, sentences, semantics, facts,information, everything.And when you feed this volume of data, obviously the model will be able to train better and able to answer questions more accurately for you.Second is size and scale.**

**So llms use massive neural networks that are called transformers, like I mentioned, and they contain billions of parameters.You can think of parameters like a knowledge bank, like a variable that is used to train the model during training.So higher the number of parameters, the better is your models and training, understanding and generation capability.Now again, GPT three, which was an older version of the 3.5 or 4 that we are using today, was trained on 175 billion parameters. Palm, which is a LM from Google, has 500.40 billion parameters.**

**Just imagine.That's why if you look at ChatGPT, for example, you ask it anything.It understands your question, it gives good answer.And the reason for that is it's training on the massive data set, like I mentioned.And this huge number of parameters base transformer, neural network.Third and last point.The training does not stop here.**

**What we saw in here was our pre-training that the models come already done with.Then we can also have some fine tuning, meaning we can further tune the LM towards a more specific and task oriented data set.We will talk about fine tuning in more depth later.**

**But just to give you an example, if we want to use an LM for text completion or summarization, we can fine tune it by exposing it to the data related to these tasks.**

**For example, I want my LM to answer data related questions related to a health care so I can train it on a health care related data set.It will make sure that the LM is more suited to your task, and it is more better at generating content for that domain or task.**

## Okay, so where can LMS be used?

**Answer is anything that involves text and in fact they are being used in many of these spaces already.First is content generation.**

**So you are in marketing advertising sales anywhere.**

**We can use LMS like ChatGPT or Lama for our text content generation.**

**Second is chat bot.**

**This is one area where LMS will make a huge impact.**

**When we are chatting with customer support, LMS can replace that first level of engagement and answer questions for you based on the company's documentation.And if the user is still not satisfied, they can go ahead and talk to a human.**

**So imagine how much effort you can save in the first place.**

**Third is language translation.**

**So there are translators already available in the market for long time, but LMS can expand on those translations and do conversation based chatting that can give you better results**

**Then we have text summarization.**

**So imagine you have a long thesis legal contract, project documentation.You don't need to read all of it.LM can generate the summary of that data for you.**

And in fact guys, I have personally created an application for it.

You can ask it for long summary, short summary, executive level summary.

It can give you all of that with amazing details and accuracy.

**And finally, Q&A, probably the most used use case.**

**We ask ChatGPT for any question and give.It gives us the pointed answer.Imagine that if I want to know who won the Superbowl 2020, I do not have to go into Wikipedia and read a long document.**

**I can just ask that question and get pointed answer in the practical learning part of this course.**

Later we will actually be creating a chatbot just like this and then you will see it really in action.

So guys, these were some of the use cases of LM.But remember that the list does not end here.LMS will change every way that we interact and manipulate text data.And the list of LMS is growing every day from GPT to Lama to palm to pointed LMS for auto industry finance industry.

Every day a new model is coming, and for sure we will get more and more innovative applications in the coming days.

Now that you understand what is, you know what their capability is, you will be ready to use them in your daily life and make your work smarter.Okay, so that was all about LMS.Let's move on and check out another topic in the next video.

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


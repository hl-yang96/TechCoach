# TechCoach Frontend - Vue.js Guide for Beginners

Welcome to the TechCoach Frontend! This guide is written for developers who are new to Vue.js, JavaScript, and modern frontend development. I'll walk you through everything you need to know to get started.

## 🎯 What is This?

The **TechCoach Frontend** is a **Vue.js** (pronounced "view") application that provides the user interface for our AI-powered career coaching platform. Think of it as the "face" of our application that users interact with in their web browser.

## 🚀 Getting Started (Step by Step)

### 1. Install Dependencies (First Time Only)
```bash
npm install
```
This downloads all the packages needed for our Vue.js app to work.

### 2. Start Development Server
```bash
npm run dev
```
This will start a local development server at http://localhost:3000

### 3. Open Your Browser
Go to `http://localhost:3000` to see your app running!

## 📁 Project Structure Explained

Think of our project like a well-organized folder structure:

```
frontend/
├── public/                 # Static files (images, HTML base template)
├── src/                    # 📂 Where all our code lives
│   ├── components/         # Reusable UI parts (buttons, forms, etc.)
│   ├── views/             # 📄 Complete pages
│   │   ├── Dashboard.vue  # Your home page
│   │   ├── Documents.vue  # Upload documents page
│   │   ├── interview/     # Interview-related pages
│   │   └── career/        # Career document pages
│   ├── router/            # 🛣️ URL routing (like /dashboard, /interview)
│   ├── services/          # 📡 API calls to backend
│   ├── stores/            # 🗄️ Global state management
│   └── App.vue            # 🔧 Main app component
├── package.json           # 📦 Project dependencies
└── vite.config.js        # ⚙️ Build configuration
```

## 🧱 Vue.js Basics (In Simple Terms)

### What is Vue.js?
Vue.js is a **JavaScript framework** that helps us build interactive web applications. Think of it as a toolkit for creating reusable components, managing data, and making websites dynamic.

### Basic Concepts Analogy:
- **Components** = LEGO blocks that we can reuse
- **Templates** = Instructions for how to display data
- **Props** = Parameters we pass to components (like function arguments)
- **State** = Data that changes and updates the interface automatically

### Example Vue Component:
```vue
<template>
  <!-- This is what users see -->
  <div class="button">
    Welcome {{ userName }}! Click count: {{ clickCount }}
  </div>
</template>

<script>
export default {
  name: 'WelcomeButton',
  data() {
    return {
      userName: 'Developer',
      clickCount: 0
    }
  }
}
</script>

<style>
.button {
  color: blue;
  padding: 10px;
}
</style>
```

## 🛣️ Routing (How Navigation Works)

Our app uses **Vue Router** to handle navigation between different pages:

- `/` → Dashboard (home page)
- `/interview` → Interview preparation page
- `/career` → Career document management
- `/upload` → Document upload page

Each route loads a **.vue** file from the `views/` folder.

## 🧪 Common Commands

| Command | Purpose | Use This For |
|---------|---------|--------------|
| `npm run dev` | Start development server | Daily development |
| `npm run build` | Create production build | Deploying the app |
| `npm run preview` | Preview production build | Testing builds locally |
| `npm run lint` | Check code quality | Keeping code clean |

## 🔄 Working with the Backend (API Calls)

Our frontend talks to the Python backend (running at http://localhost:8001) using **HTTP requests**. The frontend automatically forwards API calls starting with `/api` to the backend.

### Example API Usage:
```javascript
// From any .vue file in views/
const response = await axios.get('/api/interview/sessions')
const sessions = response.data
```

## 🎨 Styling with Tailwind CSS

We use **Tailwind CSS** for styling - it's like having ready-made CSS classes. Instead of writing custom CSS, we use pre-defined classes:

```vue
<!-- Examples of Tailwind classes -->
<div class="bg-blue-500 text-white p-4 rounded-lg">
  This creates a blue box with white text and rounded corners
</div>

<div class="flex justify-center items-center h-screen">
  Center content both horizontally and vertically
</div>
```

## 🗄️ State Management with Pinia

**Pinia** helps us manage data that needs to be shared across different parts of the app:

```javascript
// Example store (in stores/ folder)
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    currentUser: null,
    isLoggedIn: false
  }),
  actions: {
    login(user) {
      this.currentUser = user
      this.isLoggedIn = true
    }
  }
})
```

Then use in components:
```vue
<script>
import { useUserStore } from '@/stores/user'

export default {
  setup() {
    const userStore = useUserStore()
    return { userStore }
  }
}
</script>
```

## 🐛 Common Issues and Solutions

**Problem: "File not found" errors**
- ✅ Check if the file exists in the expected location
- ✅ Use the `@` symbol for the `src/` directory: `@/views/Dashboard.vue`

**Problem: Backend API calls failing**
- ✅ Make sure the backend server is running on http://localhost:8001
- ✅ Check the network tab in browser developer tools

**Problem: Styles not applying**
- ✅ Restart the development server after installing packages
- ✅ Check if Tailwind classes are spelled correctly (they're case-sensitive)

## 🎯 Next Steps for Beginners

1. **Open the Dashboard.vue** file and see the basic structure
2. **Try adding your name** to the welcome message
3. **Create a new page** by copying an existing .vue file
4. **Add a button** that shows an alert when clicked
5. **Learn by example** - look at existing views to understand patterns

## 📚 Resources to Learn More

- **Vue.js Official Tutorial**: [vuejs.org/tutorial](https://vuejs.org/tutorial/)
- **Tailwind CSS**: [tailwindcss.com/docs](https://tailwindcss.com/docs)
- **Pinia** (State Management): [pinia.vuejs.org](https://pinia.vuejs.org)
- **Vue Router**: [router.vuejs.org](https://router.vuejs.org)

## 💡 Tips for Success

1. **Start small** - modify existing components before creating new ones
2. **Use Vue DevTools** browser extension - it's like having superpowers for debugging
3. **Read error messages** - they're usually helpful and tell you exactly what's wrong
4. **Don't memorize** - focus on understanding concepts and patterns
5. **Ask for help** when stuck - Vue has a great community

---

🎉 **You're ready to start!** Try running `npm run dev` and explore the localhost:3000 app. You've got this!
import { memo } from 'react';

export const About = memo(function About() {
  const technologies = [
    { category: 'Frontend', items: ['React 18', 'TypeScript', 'Tailwind CSS', 'Vite'], color: 'blue' },
    { category: 'Backend', items: ['FastAPI', 'Python 3.11', 'Pydantic', 'Uvicorn'], color: 'green' },
    { category: 'Machine Learning', items: ['Scikit-learn', 'Naive Bayes', 'NLP', 'Pandas'], color: 'purple' },
    { category: 'Cloud & DevOps', items: ['AWS EC2', 'AWS S3', 'Docker', 'Nginx'], color: 'orange' },
    { category: 'Base de Datos', items: ['PostgreSQL', 'SQLAlchemy', 'AWS RDS'], color: 'cyan' },
  ];

  const mlModels = [
    {
      name: 'Sistema de Recomendación',
      algorithm: 'Gaussian Naive Bayes',
      description: 'Predice restaurantes basado en ubicación, preferencias y categorías gastronómicas.',
      metrics: { accuracy: '85.2%', precision: '84.7%', recall: '83.9%' }
    },
    {
      name: 'Análisis de Sentimientos',
      algorithm: 'Multinomial Naive Bayes + TF-IDF',
      description: 'Clasifica reseñas de restaurantes en sentimientos positivos, negativos o neutrales.',
      metrics: { accuracy: '87.3%', precision: '86.5%', recall: '85.8%' }
    }
  ];

  const stats = [
    { label: 'Restaurantes', value: '1,052', icon: '🍽️' },
    { label: 'Reseñas Analizadas', value: '185,666', icon: '💬' },
    { label: 'Distritos de Lima', value: '7', icon: '📍' },
    { label: 'Categorías', value: '14', icon: '🏷️' },
  ];

  const features = [
    {
      icon: '🎯',
      title: 'Recomendaciones Personalizadas',
      description: 'Algoritmo ML que aprende de tus preferencias para sugerir restaurantes ideales.'
    },
    {
      icon: '🧠',
      title: 'Análisis de Sentimientos',
      description: 'Procesamiento de lenguaje natural para evaluar reseñas automáticamente.'
    },
    {
      icon: '📍',
      title: 'Búsqueda por Ubicación',
      description: 'Encuentra restaurantes cercanos usando geolocalización.'
    },
    {
      icon: '⚡',
      title: 'Tiempo Real',
      description: 'Respuestas instantáneas con inferencia ML optimizada.'
    }
  ];

  return (
    <div className="min-h-full bg-gradient-to-br from-gray-50 to-blue-50 pb-8">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="flex flex-col md:flex-row items-center gap-8">
            <div className="w-24 h-24 bg-white/20 rounded-3xl flex items-center justify-center backdrop-blur-sm">
              <span className="text-5xl">🍽️</span>
            </div>
            <div className="text-center md:text-left">
              <h1 className="text-4xl md:text-5xl font-bold mb-3">FoodieAI</h1>
              <p className="text-xl text-blue-100 max-w-2xl">
                Sistema Inteligente de Recomendación de Restaurantes basado en Machine Learning
              </p>
              <div className="flex flex-wrap justify-center md:justify-start gap-3 mt-4">
                <span className="px-3 py-1 bg-white/20 rounded-full text-sm font-medium">
                  🤖 Powered by ML
                </span>
                <span className="px-3 py-1 bg-white/20 rounded-full text-sm font-medium">
                  📍 Lima, Perú
                </span>
                <span className="px-3 py-1 bg-white/20 rounded-full text-sm font-medium">
                  v2.0.0
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {stats.map((stat) => (
            <div key={stat.label} className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 text-center hover:shadow-md transition-shadow">
              <div className="text-4xl mb-2">{stat.icon}</div>
              <div className="text-3xl font-bold text-gray-900">{stat.value}</div>
              <div className="text-sm text-gray-500 mt-1">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Features Section */}
        <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-3">
            <span className="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center">
              <span className="text-xl">✨</span>
            </span>
            Características Principales
          </h2>
          <div className="grid md:grid-cols-2 gap-6">
            {features.map((feature) => (
              <div key={feature.title} className="flex gap-4 p-4 rounded-xl bg-gray-50 hover:bg-blue-50 transition-colors">
                <div className="w-12 h-12 bg-white rounded-xl flex items-center justify-center shadow-sm flex-shrink-0">
                  <span className="text-2xl">{feature.icon}</span>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">{feature.title}</h3>
                  <p className="text-sm text-gray-600 mt-1">{feature.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* ML Models Section */}
        <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-3">
            <span className="w-10 h-10 bg-purple-100 rounded-xl flex items-center justify-center">
              <span className="text-xl">🧠</span>
            </span>
            Modelos de Machine Learning
          </h2>
          <div className="grid md:grid-cols-2 gap-6">
            {mlModels.map((model) => (
              <div key={model.name} className="border border-gray-200 rounded-xl p-6 hover:border-purple-300 transition-colors">
                <h3 className="text-lg font-bold text-gray-900 mb-2">{model.name}</h3>
                <div className="inline-block px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm font-medium mb-3">
                  {model.algorithm}
                </div>
                <p className="text-gray-600 text-sm mb-4">{model.description}</p>
                <div className="grid grid-cols-3 gap-2">
                  <div className="bg-green-50 rounded-lg p-3 text-center">
                    <div className="text-lg font-bold text-green-700">{model.metrics.accuracy}</div>
                    <div className="text-xs text-green-600">Accuracy</div>
                  </div>
                  <div className="bg-blue-50 rounded-lg p-3 text-center">
                    <div className="text-lg font-bold text-blue-700">{model.metrics.precision}</div>
                    <div className="text-xs text-blue-600">Precision</div>
                  </div>
                  <div className="bg-amber-50 rounded-lg p-3 text-center">
                    <div className="text-lg font-bold text-amber-700">{model.metrics.recall}</div>
                    <div className="text-xs text-amber-600">Recall</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Technologies Section */}
        <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-3">
            <span className="w-10 h-10 bg-green-100 rounded-xl flex items-center justify-center">
              <span className="text-xl">🛠️</span>
            </span>
            Stack Tecnológico
          </h2>
          <div className="grid sm:grid-cols-2 lg:grid-cols-5 gap-4">
            {technologies.map((tech) => (
              <div key={tech.category} className="bg-gray-50 rounded-xl p-4">
                <h3 className="font-semibold text-gray-900 mb-3 text-sm">{tech.category}</h3>
                <div className="flex flex-wrap gap-2">
                  {tech.items.map((item) => (
                    <span
                      key={item}
                      className={`px-2 py-1 rounded-md text-xs font-medium ${
                        tech.color === 'blue' ? 'bg-blue-100 text-blue-700' :
                        tech.color === 'green' ? 'bg-green-100 text-green-700' :
                        tech.color === 'purple' ? 'bg-purple-100 text-purple-700' :
                        tech.color === 'orange' ? 'bg-orange-100 text-orange-700' :
                        'bg-cyan-100 text-cyan-700'
                      }`}
                    >
                      {item}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Architecture Section */}
        <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-3">
            <span className="w-10 h-10 bg-indigo-100 rounded-xl flex items-center justify-center">
              <span className="text-xl">🏗️</span>
            </span>
            Arquitectura del Sistema
          </h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-6">
              <div className="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="font-bold text-gray-900 mb-2">Frontend</h3>
              <p className="text-sm text-gray-600">
                SPA con React y TypeScript. UI responsiva con Tailwind CSS. Estado global con hooks personalizados.
              </p>
            </div>
            <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-6">
              <div className="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2" />
                </svg>
              </div>
              <h3 className="font-bold text-gray-900 mb-2">Backend API</h3>
              <p className="text-sm text-gray-600">
                REST API con FastAPI. Clean Architecture / Hexagonal. Documentación OpenAPI automática.
              </p>
            </div>
            <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-6">
              <div className="w-12 h-12 bg-purple-500 rounded-xl flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <h3 className="font-bold text-gray-900 mb-2">ML Engine</h3>
              <p className="text-sm text-gray-600">
                Modelos entrenados con Scikit-learn. Preprocesamiento con Pandas. Inferencia optimizada en memoria.
              </p>
            </div>
          </div>
        </div>

        {/* Version Info */}
        <div className="bg-gradient-to-r from-gray-800 to-gray-900 rounded-2xl p-8 text-white">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div>
              <h2 className="text-xl font-bold mb-2">FoodieAI v2.0.0</h2>
              <p className="text-gray-400 text-sm">
                Sistema de Recomendación de Restaurantes con Machine Learning
              </p>
              <p className="text-gray-500 text-xs mt-2">
                Universidad Nacional Mayor de San Marcos • Lima, Perú • 2025
              </p>
            </div>
            <div className="flex items-center gap-4">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="w-12 h-12 bg-white/10 rounded-xl flex items-center justify-center hover:bg-white/20 transition-colors"
              >
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
                </svg>
              </a>
              <div className="text-right">
                <div className="text-sm text-gray-400">Última actualización</div>
                <div className="font-medium">Diciembre 2025</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
});

export default About;

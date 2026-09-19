<template>
  <header class="site-header" id="inicio">
    <nav class="nav">
      <div class="header-logo">
        <img :src="logoSrc" alt="Logo Ótica Amancio">
      </div>

      <!-- Botão Hambúrguer Mobile -->
      <button
        class="mobile-menu-toggle"
        type="button"
        :aria-expanded="String(isMobileNavOpen)"
        aria-label="Abrir menu de navegação"
        @click="isMobileNavOpen = !isMobileNavOpen"
      >
        <span class="bar" :class="{ 'bar-top': isMobileNavOpen }"></span>
        <span class="bar" :class="{ 'bar-mid': isMobileNavOpen }"></span>
        <span class="bar" :class="{ 'bar-bot': isMobileNavOpen }"></span>
      </button>

      <!-- Links de Navegação (Desktop e gaveta Mobile) -->
      <div class="nav-links" :class="{ 'nav-open': isMobileNavOpen }">
        <a href="#catalogo" class="cata" @click="isMobileNavOpen = false">Catálogo</a>
        <a
          class="whatsapp-link"
          :href="quickWhatsAppLink"
          target="_blank"
          rel="noopener"
          @click="isMobileNavOpen = false"
        >
          WhatsApp
        </a>
      </div>
    </nav>
  </header>

  <main>
    <section class="hero">
      <div class="hero-copy">
        <p class="eyebrow">Óculos de grau e Óculos solares em Maceió</p>
        <h1>Selecione a armação ideal</h1>
        <p> e informe sua receita por foto ou pela grade OD/OE com esférico, cilindro e eixo.</p>
        <div class="hero-actions">
          <a class="primary-button" href="#catalogo">Ver armações</a>
          <a class="secondary-button" :href="quickWhatsAppLink" target="_blank" rel="noopener">{{ orderIntentText }}</a>
        </div>
      </div>
      <div class="hero-showcase" aria-label="Armações em destaque">
        <div class="hero-carousel">
          <button class="carousel-arrow prev" type="button" aria-label="Imagem anterior" @click="previousFeaturedImage">‹</button>
          <img
            :key="activeFeaturedImage.src"
            :src="activeFeaturedImage.src"
            :alt="activeFeaturedImage.alt"
            @click="openImage(activeFeaturedImage.src)"
          >
          <button class="carousel-arrow next" type="button" aria-label="Próxima imagem" @click="nextFeaturedImage">›</button>

          <div class="carousel-dots" aria-label="Selecionar imagem em destaque">
            <button
              v-for="(image, index) in featuredImages"
              :key="image.src"
              type="button"
              :class="{ active: currentFeaturedIndex === index }"
              :aria-label="`Ver imagem ${index + 1}`"
              @click="setFeaturedImage(index)"
            ></button>
          </div>
        </div>
      </div>
    </section>

    <section class="notice-grid" id="receita">
      <article class="notice important">
        <span class="notice-icon">!</span>
        <div>
          <h2>Atenção para lente multifocal</h2>
          <p>Se o grau for multifocal, lente para perto e longe, é necessário fazer a marcação da distância naso-pupilar, também conhecida como DNP.</p>
        </div>
      </article>

      <article class="notice" id="visita">
        <span class="notice-icon">✓</span>
        <div>
          <h2>Visita em toda Maceió</h2>
          <p>Fazemos visita caso você tenha dúvida sobre qual armação levar ou queira ver como o modelo fica melhor no seu rosto.</p>
        </div>
      </article>
    </section>

    <section class="catalog-section" id="catalogo">
      <div class="section-heading">
        <p class="eyebrow">Catálogo</p>
        <h2>Nossas Armações</h2>
        <p>Toque em uma categoria para ver os modelos e depois escolha a armação para enviar a receita.</p>
      </div>

      <button
        class="mobile-filter-toggle"
        type="button"
        :aria-expanded="String(isMobileFiltersOpen)"
        aria-controls="catalog-filters"
        @click="isMobileFiltersOpen = !isMobileFiltersOpen"
      >
        <span class="mobile-filter-label">
          <span class="mobile-filter-icon" aria-hidden="true">☰</span>
          Filtros
        </span>
        <span class="mobile-filter-status">
          {{ activeFilter === "todos" ? "Todos" : categories[activeFilter] }}
          <span class="mobile-filter-chevron" :class="{ rotated: isMobileFiltersOpen }" aria-hidden="true">⌄</span>
        </span>
      </button>

      <div
        id="catalog-filters"
        class="filters"
        :class="{ 'mobile-open': isMobileFiltersOpen }"
        role="tablist"
        aria-label="Categorias de armações"
      >
        <button
          v-for="filter in filters"
          :key="filter.value"
          class="filter-button"
          :class="{ active: activeFilter === filter.value }"
          type="button"
          role="tab"
          :aria-selected="String(activeFilter === filter.value)"
          @click="selectFilter(filter.value)"
        >
          {{ filter.label }}
        </button>

        <button
          v-if="activeFilter !== 'todos'"
          class="clear-filter-button"
          type="button"
          @click="selectFilter('todos')"
        >
          Limpar filtro
        </button>
      </div>

      <div v-if="filteredProducts.length" class="catalog-grid" aria-live="polite">
        <article v-for="product in filteredProducts" :key="product.id" class="product-card">
          <div class="product-media">
            <span class="tag">{{ categories[product.category] }}</span>
            <img :src="product.image" :alt="product.name" @click="openImage(product.image)">
          </div>
          <div class="product-content">
            <h3>{{ product.name }}</h3>
            <p>{{ product.description }}</p>
            <div class="price-row">
              <span class="price">{{ product.price }}</span>
              <span class="badge">Armação disponível</span>
            </div>
            <div class="product-actions">
              <button class="icon-button" type="button" :aria-label="`Ampliar ${product.name}`" @click="openImage(product.image)">⌕</button>
              <button class="choose-button" type="button" @click="openOrderPanel(product)">Escolher armação</button>
            </div>
          </div>
        </article>
      </div>

      <p v-else class="empty-state">Nenhuma armação encontrada nesta categoria.</p>
    </section>
  </main>

  <aside class="order-panel" :class="{ open: isOrderPanelOpen }" :aria-hidden="String(!isOrderPanelOpen)" @click.self="closeOrderPanel">
    <div v-if="selectedProduct" class="order-card" role="dialog" aria-modal="true" aria-labelledby="orderTitle">
      <button class="close-button" type="button" @click="closeOrderPanel" aria-label="Fechar">×</button>
      <div class="selected-product">
        <img :src="selectedProduct.image" :alt="selectedProduct.name">
        <div>
          <p class="eyebrow">Armação escolhida</p>
          <h2 id="orderTitle">{{ selectedProduct.name }}</h2>
          <p class="selected-category-text">{{ categories[selectedProduct.category] }}</p>
        </div>
      </div>

      <form @submit.prevent="sendOrder">
        <fieldset>
          <legend>Envio da receita</legend>
          <label class="check-row">
            <input type="checkbox" v-model="form.hasRecipePhoto">
            Vou enviar foto da consulta/receita pelo WhatsApp
          </label>
          <label class="check-row">
            <input type="checkbox" v-model="form.isMultifocal">
            Meu grau é multifocal
          </label>
          <p class="form-note">Para multifocal, a Ótica Amancio fará a orientação da marcação de DNP.</p>
        </fieldset>

        <fieldset class="prescription-grid">
          <legend>Grade do grau</legend>
          <div class="grid-head"></div>
          <div class="grid-head">Esférico</div>
          <div class="grid-head">Cilindro</div>
          <div class="grid-head">Eixo</div>

          <label class="eye-label" for="odSphere">OD</label>
          <select id="odSphere" v-model="form.od.sphere">
            <option v-for="option in sphereOptions" :key="`od-sphere-${option.value}`" :value="option.value">{{ option.label }}</option>
          </select>
          <select v-model="form.od.cylinder">
            <option v-for="option in cylinderOptions" :key="`od-cylinder-${option.value}`" :value="option.value">{{ option.label }}</option>
          </select>
          <select v-model="form.od.axis">
            <option v-for="option in axisOptions" :key="`od-axis-${option.value}`" :value="option.value">{{ option.label }}</option>
          </select>

          <label class="eye-label" for="oeSphere">OE</label>
          <select id="oeSphere" v-model="form.oe.sphere">
            <option v-for="option in sphereOptions" :key="`oe-sphere-${option.value}`" :value="option.value">{{ option.label }}</option>
          </select>
          <select v-model="form.oe.cylinder">
            <option v-for="option in cylinderOptions" :key="`oe-cylinder-${option.value}`" :value="option.value">{{ option.label }}</option>
          </select>
          <select v-model="form.oe.axis">
            <option v-for="option in axisOptions" :key="`oe-axis-${option.value}`" :value="option.value">{{ option.label }}</option>
          </select>
        </fieldset>

        <label class="text-label" for="observations">Observações: </label>
        <textarea id="observations" v-model.trim="form.observations" rows="3" placeholder="Ex: tenho dúvida no tamanho, quero visita em Maceió, preferência de cor..."></textarea>

        <button class="primary-button full" type="submit">Enviar pedido no WhatsApp</button>
      </form>
    </div>
  </aside>

  <div id="lightbox" :class="{ open: lightboxImage }" :aria-hidden="String(!lightboxImage)" @click="closeImage">
    <img v-if="lightboxImage" :src="lightboxImage" alt="Imagem ampliada">
  </div>

  <footer>
    <strong>Ótica Amancio</strong>
    <p>Catálogo online de armações. Atendimento e visitas em Maceió.</p>
    <div class="footer-actions">
      <a :href="quickWhatsAppLink" target="_blank" rel="noopener">WhatsApp</a>
      <a href="#catalogo" class="cat">Ver catálogo</a>
    </div>
    <small>© 2026 Ótica Amancio. Todos os direitos reservados.</small>
  </footer>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue";

const whatsappNumber = "5582991200198";
const orderIntentText = "Enviar meu grau e receber avaliação";
const activeFilter = ref("todos");
const isMobileFiltersOpen = ref(false);
const selectedProduct = ref(null);
const isOrderPanelOpen = ref(false);
const currentFeaturedIndex = ref(0);
const lightboxImage = ref(null);
const isMobileNavOpen = ref(false);
let carouselTimer = null;

const openImage = (src) => {
  lightboxImage.value = src;
};

const closeImage = () => {
  lightboxImage.value = null;
};

const categories = {
  polarizadas: "Polarizadas",
  "masculina-metal": "Masculina metal",
  "masculina-acetato": "Masculina acetato",
  "masculina-classica": "Masculina clássica",
  "masculina-oakley": "Masculina esportiva",
  unissex: "Unissex"
};

const imagePath = (fileName) => new URL(`../img/${fileName}`, import.meta.url).href;
const logoSrc = imagePath("logo-kim-otica.png");

const products = [
  {
    id: "oa-m001",
    name: "Dobravel 1",
    category: "masculina-acetato",
    image: imagePath("masc-acetato-dobravel-1.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina em acetato, resistente e confortável para uso diário."
  },
  {
    id: "oa-m002",
    name: "Dobravel 2",
    category: "masculina-acetato",
    image: imagePath("masc-acetato-dobravel-2.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina em acetato, resistente e confortável para uso diário."
  },
  {
    id: "oa-m003",
    name: "Oakley Pitchman MARROM",
    category: "masculina-acetato",
    image: imagePath("masc-acetato-oakley-pitchman-marrom.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina em acetato, resistente e confortável para uso diário."
  },
  {
    id: "oa-m004",
    name: "Oakley Pitchman PRETO",
    category: "masculina-acetato",
    image: imagePath("masc-acetato-oakley-pitchman-preto.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina em acetato, resistente e confortável para uso diário."
  },
  {
    id: "oa-m005",
    name: "Estilo Juliete",
    category: "masculina-classica",
    image: imagePath("masc-estilo-juliete-estilo-juliete.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina de estilo clássico, confortável para uso prolongado."
  },
  {
    id: "oa-m006",
    name: "Juliete",
    category: "masculina-classica",
    image: imagePath("masc-juliete-juliete.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina de estilo clássico, confortável para uso prolongado."
  },
  {
    id: "oa-m007",
    name: "Metal Fina Prata Climpom(Preto)(Marrom)",
    category: "masculina-metal",
    image: imagePath("masc-metal-metal-fina-prata-climpom-preto-marrom.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina em metal, leve e com acabamento resistente."
  },
  {
    id: "oa-m008",
    name: "Metal Prada 1",
    category: "masculina-metal",
    image: imagePath("masc-metal-metal-prada-1.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina em metal, leve e com acabamento resistente."
  },
  {
    id: "oa-m009",
    name: "Metal Prada 2",
    category: "masculina-metal",
    image: imagePath("masc-metal-metal-prada-2.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina em metal, leve e com acabamento resistente."
  },
  {
    id: "oa-m010",
    name: "Metal Prata Clipom (Preto)(Night Drive)",
    category: "masculina-metal",
    image: imagePath("masc-metal-metal-prata-clipom-preto-night-drive.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina em metal, leve e com acabamento resistente."
  },
  {
    id: "oa-m011",
    name: "Metal Prata Clipom Preto",
    category: "masculina-metal",
    image: imagePath("masc-metal-metal-prata-clipom-preto.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina em metal, leve e com acabamento resistente."
  },
  {
    id: "oa-m012",
    name: "Metal Prata Semiflutuante Clipom Preto",
    category: "masculina-metal",
    image: imagePath("masc-metal-metal-prata-semiflutuante-clipom-preto.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina em metal, leve e com acabamento resistente."
  },
  {
    id: "oa-m013",
    name: "Metal Preta 2 Clipom Preto",
    category: "masculina-metal",
    image: imagePath("masc-metal-metal-preta-2-clipom-preto.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina em metal, leve e com acabamento resistente."
  },
  {
    id: "oa-m014",
    name: "Metal Preta Clipom (Preto)(Night Drive)",
    category: "masculina-metal",
    image: imagePath("masc-metal-metal-preta-clipom-preto-night-drive.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina em metal, leve e com acabamento resistente."
  },
  {
    id: "oa-m015",
    name: "Metal Preta Clipom Preto",
    category: "masculina-metal",
    image: imagePath("masc-metal-metal-preta-clipom-preto.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina em metal, leve e com acabamento resistente."
  },
  {
    id: "oa-m016",
    name: "Oakley Prata Semi Flutuante",
    category: "masculina-metal",
    image: imagePath("masc-metal-oakley-prata-semi-flutuante.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina em metal, leve e com acabamento resistente."
  },
  {
    id: "oa-m017",
    name: "Ray Ban",
    category: "masculina-metal",
    image: imagePath("masc-metal-ray-ban.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina em metal, leve e com acabamento resistente."
  },
  {
    id: "oa-m018",
    name: "Rayban +Ferrari",
    category: "masculina-metal",
    image: imagePath("masc-metal-rayban-ferrari.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina em metal, leve e com acabamento resistente."
  },
  {
    id: "oa-m019",
    name: "Oakley Batwolf",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-batwolf-oakley-batwolf.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m020",
    name: "Oakley Eye Jacket Azul Claro",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-eye-jacket-oakley-eye-jacket-azul-claro.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m021",
    name: "Oakley Eye Jacket Azul Escuro",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-eye-jacket-oakley-eye-jacket-azul-escuro.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m022",
    name: "Oakley Plate 1 Azul Claro",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-plate-oakley-plate-1-azul-claro.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m023",
    name: "Oakley Plate Amarelo",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-plate-oakley-plate-amarelo.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m024",
    name: "Oakley Plate Azul Claro Com Detalhe Verde",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-plate-oakley-plate-azul-claro-com-detalhe-verde.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m025",
    name: "Oakley Plate Azul Escuro",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-plate-oakley-plate-azul-escuro.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m026",
    name: "Oakley Plate Prata",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-plate-oakley-plate-prata.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m027",
    name: "Oakley Plate Modelo 1",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-plate-modelo-1.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m028",
    name: "Oakley Plate Modelo 2",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-plate-modelo-2.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m029",
    name: "Oakley Plate Modelo 3",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-plate-modelo-3.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m030",
    name: "Oakley Plate Modelo 4",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-plate-modelo-4.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m031",
    name: "Oakley Plate Modelo 5",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-plate-modelo-5.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m032",
    name: "Oakley Plate Modelo 6",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-plate-modelo-6.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m033",
    name: "Oakley Plate Modelo 7",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-plate-modelo-7.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m034",
    name: "Oakley Plate Modelo 8",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-plate-modelo-8.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m035",
    name: "Oakley Plate Modelo 9",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-plate-modelo-9.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m036",
    name: "Oakley Plate Modelo 10",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-plate-modelo-10.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m037",
    name: "Oakley Radar Prateado",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-radar-oakley-radar-prateado.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m038",
    name: "Oakley Radar Preto Azulado",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-radar-oakley-radar-preto-azulado.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m039",
    name: "Oakley Radar Preto-Prata",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-radar-oakley-radar-preto-prata.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m040",
    name: "Oakley Radar Total Black",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-radar-oakley-radar-total-black.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m041",
    name: "Oakley 1",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-twoface-oakley-1.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m042",
    name: "Vilão 1",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-vilao-vilao-1.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m043",
    name: "Vilão 2",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-vilao-vilao-2.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m044",
    name: "Vilão 3",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-vilao-vilao-3.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m045",
    name: "Vilão 4",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-vilao-vilao-4.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m046",
    name: "Vilão 5",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-vilao-vilao-5.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m047",
    name: "Vilão 6",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-vilao-vilao-6.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m048",
    name: "Vilão 7",
    category: "masculina-oakley",
    image: imagePath("masc-oakley-vilao-vilao-7.jpg"),
    price: "R$ 120,00",
    description: "Armação esportiva masculina, ideal para quem busca resistência e estilo."
  },
  {
    id: "oa-m049",
    name: "Oakley 1",
    category: "masculina-classica",
    image: imagePath("masc-parafusada-oakley-1.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina de estilo clássico, confortável para uso prolongado."
  },
  {
    id: "oa-m050",
    name: "Oakley 2",
    category: "masculina-classica",
    image: imagePath("masc-parafusada-oakley-2.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina de estilo clássico, confortável para uso prolongado."
  },
  {
    id: "oa-m051",
    name: "Oakley 3",
    category: "masculina-classica",
    image: imagePath("masc-parafusada-oakley-3.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina de estilo clássico, confortável para uso prolongado."
  },
  {
    id: "oa-m052",
    name: "Oakley 4",
    category: "masculina-classica",
    image: imagePath("masc-parafusada-oakley-4.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina de estilo clássico, confortável para uso prolongado."
  },
  {
    id: "oa-m053",
    name: "Oakley 5",
    category: "masculina-classica",
    image: imagePath("masc-parafusada-oakley-5.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina de estilo clássico, confortável para uso prolongado."
  },
  {
    id: "oa-m054",
    name: "Oakley 6",
    category: "masculina-classica",
    image: imagePath("masc-parafusada-oakley-6.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina de estilo clássico, confortável para uso prolongado."
  },
  {
    id: "oa-m055",
    name: "Parafusada 1",
    category: "masculina-classica",
    image: imagePath("masc-parafusada-parafusada-1.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina de estilo clássico, confortável para uso prolongado."
  },
  {
    id: "oa-m056",
    name: "Parafusada 2",
    category: "masculina-classica",
    image: imagePath("masc-parafusada-parafusada-2.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina de estilo clássico, confortável para uso prolongado."
  },
  {
    id: "oa-m057",
    name: "Parafusada 3",
    category: "masculina-classica",
    image: imagePath("masc-parafusada-parafusada-3.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina de estilo clássico, confortável para uso prolongado."
  },
  {
    id: "oa-m058",
    name: "Parafusada 4",
    category: "masculina-classica",
    image: imagePath("masc-parafusada-parafusada-4.jpg"),
    price: "R$ 120,00",
    description: "Armação masculina de estilo clássico, confortável para uso prolongado."
  },
  {
    id: "oa-u059",
    name: "Modelo 1",
    category: "unissex",
    image: imagePath("uni-modelo-1.jpg"),
    price: "R$ 120,00",
    description: "Armação unissex versátil, confortável para o dia a dia."
  },
  {
    id: "oa-u060",
    name: "Modelo 2",
    category: "unissex",
    image: imagePath("uni-modelo-2.jpg"),
    price: "R$ 120,00",
    description: "Armação unissex versátil, confortável para o dia a dia."
  },
  {
    id: "oa-u061",
    name: "Modelo 3",
    category: "unissex",
    image: imagePath("uni-modelo-3.jpg"),
    price: "R$ 120,00",
    description: "Armação unissex versátil, confortável para o dia a dia."
  },
  {
    id: "oa-u062",
    name: "Modelo 4",
    category: "unissex",
    image: imagePath("uni-modelo-4.jpg"),
    price: "R$ 120,00",
    description: "Armação unissex versátil, confortável para o dia a dia."
  },
  {
    id: "oa-u063",
    name: "Modelo 5",
    category: "unissex",
    image: imagePath("uni-modelo-5.jpg"),
    price: "R$ 120,00",
    description: "Armação復unissex versátil, confortável para o dia a dia."
  },
  {
    id: "oa-u064",
    name: "Modelo 6",
    category: "unissex",
    image: imagePath("uni-modelo-6.jpg"),
    price: "R$ 120,00",
    description: "Armação unissex versátil, confortável para o dia a dia."
  },
  {
    id: "oa-u065",
    name: "Modelo 7",
    category: "unissex",
    image: imagePath("uni-modelo-7.jpg"),
    price: "R$ 120,00",
    description: "Armação unissex versátil, confortável para o dia a dia."
  },
  {
    id: "oa-u066",
    name: "Modelo 8",
    category: "unissex",
    image: imagePath("uni-modelo-8.jpg"),
    price: "R$ 120,00",
    description: "Armação unissex versátil, confortável para o dia a dia."
  },
  {
    id: "oa-u067",
    name: "Modelo 9",
    category: "unissex",
    image: imagePath("uni-modelo-9.jpg"),
    price: "R$ 120,00",
    description: "Armação unissex versátil, confortável para o dia a dia."
  },
  {
    id: "oa-u068",
    name: "Modelo 10",
    category: "unissex",
    image: imagePath("uni-modelo-10.jpg"),
    price: "R$ 120,00",
    description: "Armação unissex versátil, confortável para o dia a dia."
  },
  {
    id: "oa-u069",
    name: "Modelo 11",
    category: "unissex",
    image: imagePath("uni-modelo-11.jpg"),
    price: "R$ 120,00",
    description: "Armação unissex versátil, confortável para o dia a dia."
  },
  {
    id: "oa-u070",
    name: "Modelo 12",
    category: "unissex",
    image: imagePath("uni-modelo-12.jpg"),
    price: "R$ 120,00",
    description: "Armação unissex versátil, confortável para o dia a dia."
  },
  {
    id: "oa-u071",
    name: "Modelo 13",
    category: "unissex",
    image: imagePath("uni-modelo-13.jpg"),
    price: "R$ 120,00",
    description: "Armação unissex versátil, confortável para o dia a dia."
  },
  {
    id: "oa-u072",
    name: "Modelo 14",
    category: "unissex",
    image: imagePath("uni-modelo-14.jpg"),
    price: "R$ 120,00",
    description: "Armação unissex versátil, confortável para o dia a dia."
  },
  {
    id: "oa-u073",
    name: "Modelo 15",
    category: "unissex",
    image: imagePath("uni-modelo-15.jpg"),
    price: "R$ 120,00",
    description: "Armação unissex versátil, confortável para o dia a dia."
  },
  {
    id: "oa-u074",
    name: "Modelo 16",
    category: "unissex",
    image: imagePath("uni-modelo-16.jpg"),
    price: "R$ 120,00",
    description: "Armação unissex versátil, confortável para o dia a dia."
  },
  {
    id: "oa-u075",
    name: "Modelo 18",
    category: "unissex",
    image: imagePath("uni-modelo-18.jpg"),
    price: "R$ 120,00",
    description: "Armação unissex versátil, confortável para o dia a dia."
  },
  {
    id: "oa-u076",
    name: "Modelo 19",
    category: "unissex",
    image: imagePath("uni-modelo-19.jpg"),
    price: "R$ 120,00",
    description: "Armação unissex versátil, confortável para o dia a dia."
  },
  {
    id: "oa-u077",
    name: "Modelo 20",
    category: "unissex",
    image: imagePath("uni-modelo-20.jpg"),
    price: "R$ 120,00",
    description: "Armação unissex versátil, confortável para o dia a dia."
  },
  {
    id: "oa-u078",
    name: "Modelo 21",
    category: "unissex",
    image: imagePath("uni-modelo-21.jpg"),
    price: "R$ 120,00",
    description: "Armação unissex versátil, confortável para o dia a dia."
  }
];

const featuredImages = [
  {
    src: imagePath("masc-oakley-vilao-vilao-1.jpg"),
    alt: "Armação Oakley Vilão em destaque"
  },
  {
    src: imagePath("uni-modelo-19.jpg"),
    alt: "Armação unissex em destaque"
  },
  {
    src: imagePath("masc-metal-rayban-ferrari.jpg"),
    alt: "Armação metálica em destaque"
  }
];

const activeFeaturedImage = computed(() => featuredImages[currentFeaturedIndex.value]);

const initialPrescriptionForm = () => ({
  hasRecipePhoto: false,
  isMultifocal: false,
  observations: "",
  od: {
    sphere: "0.00",
    cylinder: "0.00",
    axis: "0°"
  },
  oe: {
    sphere: "0.00",
    cylinder: "0.00",
    axis: "0°"
  }
});

const form = ref(initialPrescriptionForm());

const filters = computed(() => [
  { value: "todos", label: "Todos" },
  ...Object.entries(categories).map(([value, label]) => ({ value, label }))
]);

const selectFilter = (value) => {
  activeFilter.value = value;
  isMobileFiltersOpen.value = false;
};

const filteredProducts = computed(() => {
  if (activeFilter.value === "todos") return products;
  return products.filter((product) => product.category === activeFilter.value);
});

const formatDegree = (value, showPlus = true) => {
  if (value === 0) return "0.00";
  const signal = value > 0 && showPlus ? "+" : "";
  return `${signal}${value.toFixed(2)}`;
};

const sphereOptions = computed(() => {
  const values = [0];
  for (let value = 0.25; value <= 6.001; value += 0.25) values.push(value);
  for (let value = -0.25; value >= -5.001; value -= 0.25) values.push(value);

  return values.map((value) => ({
    value: formatDegree(value),
    label: value === 0 ? "Sem grau / 0.00" : formatDegree(value)
  }));
});

const cylinderOptions = computed(() => {
  const values = [0];
  for (let value = -0.25; value >= -4.001; value -= 0.25) values.push(value);

  return values.map((value) => ({
    value: formatDegree(value, false),
    label: value === 0 ? "Sem cilindro / 0.00" : formatDegree(value, false)
  }));
});

const axisOptions = computed(() => {
  const values = [];
  for (let value = 0; value <= 180; value += 5) values.push(value);

  return values.map((value) => ({
    value: `${value}°`,
    label: value === 0 ? "0° ou 180°" : `${value}°`
  }));
});

const whatsAppLink = (message) => `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(message)}`;
const quickWhatsAppLink = computed(() => whatsAppLink("Olá, Tenho uma receita de vista e quero fazer um orçamento de armação + lente. Como faço para enviar?"));

const openOrderPanel = (product) => {
  selectedProduct.value = product;
  form.value = initialPrescriptionForm();
  isOrderPanelOpen.value = true;
};

const closeOrderPanel = () => {
  isOrderPanelOpen.value = false;
};

const setFeaturedImage = (index) => {
  currentFeaturedIndex.value = index;
  restartCarousel();
};

const nextFeaturedImage = () => {
  currentFeaturedIndex.value = (currentFeaturedIndex.value + 1) % featuredImages.length;
  restartCarousel();
};

const previousFeaturedImage = () => {
  currentFeaturedIndex.value = (currentFeaturedIndex.value - 1 + featuredImages.length) % featuredImages.length;
  restartCarousel();
};

const startCarousel = () => {
  carouselTimer = window.setInterval(() => {
    currentFeaturedIndex.value = (currentFeaturedIndex.value + 1) % featuredImages.length;
  }, 4500);
};

const stopCarousel = () => {
  if (carouselTimer) {
    window.clearInterval(carouselTimer);
    carouselTimer = null;
  }
};

const restartCarousel = () => {
  stopCarousel();
  startCarousel();
};

const prescriptionText = () => [
  `OD: Esférico ${form.value.od.sphere} | Cilindro ${form.value.od.cylinder} | Eixo ${form.value.od.axis}`,
  `OE: Esférico ${form.value.oe.sphere} | Cilindro ${form.value.oe.cylinder} | Eixo ${form.value.oe.axis}`
].join("\n");

const sendOrder = () => {
  if (!selectedProduct.value) return;

  const message = [
    "Olá, gostaria de atendimento da Ótica Amancio.",
    orderIntentText,
    "",
    `Armação escolhida: ${selectedProduct.value.name}`,
    `Categoria: ${categories[selectedProduct.value.category]}`,
    `Imagem: ${selectedProduct.value.image}`,
    "Review da imagem: quero que vocês avaliem essa armação pela imagem e me orientem se ela combina com meu rosto e com o meu grau.",
    "",
    form.value.hasRecipePhoto
      ? "Vou enviar a foto da consulta/receita pelo WhatsApp."
      : "Preenchi meu grau pela grade:",
    form.value.hasRecipePhoto ? "" : prescriptionText(),
    form.value.isMultifocal
      ? "Meu grau é multifocal. Preciso de orientação para marcação da DNP."
      : "Meu grau não é multifocal.",
    form.value.observations ? `Observações: ${form.value.observations}` : ""
  ].filter(Boolean).join("\n");

  window.open(whatsAppLink(message), "_blank");
};

onMounted(() => {
  startCarousel();

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeOrderPanel();
      closeImage();
    }
  });
});

onBeforeUnmount(() => {
  stopCarousel();
});
</script>

<style scoped>
.site-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
}

.nav {
  max-width: 1200px;
  margin: 0 auto;
  padding: 12px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
}

.header-logo img {
  height: 42px;
  width: auto;
  display: block;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 16px;
}

.nav-links a {
  text-decoration: none;
  font-weight: 700;
  color: #1f2937;
  font-size: 0.95rem;
}

.whatsapp-link {
  background: #25d366;
  color: #ffffff !important;
  padding: 8px 16px;
  border-radius: 8px;
}

.hero {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: center;
}

.eyebrow {
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 1px;
  color: #6b7280;
  font-weight: 700;
  margin-bottom: 8px;
}

.hero-copy h1 {
  font-size: 2.5rem;
  line-height: 1.15;
  color: #111827;
  margin-bottom: 12px;
}

.hero-copy p {
  color: #4b5563;
  line-height: 1.5;
  margin-bottom: 24px;
}

.hero-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.primary-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #111827;
  color: #ffffff;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 700;
  text-decoration: none;
  border: none;
  cursor: pointer;
}

.secondary-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #f3f4f6;
  color: #111827;
  padding: 12px 20px;
  border-radius: 8px;
  font-weight: 700;
  text-decoration: none;
}

.hero-carousel {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  background: #f3f4f6;
}

.hero-carousel img {
  width: 100%;
  height: 380px;
  object-fit: cover;
  display: block;
  cursor: pointer;
}

.carousel-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.85);
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  font-size: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.carousel-arrow.prev {
  left: 12px;
}

.carousel-arrow.next {
  right: 12px;
}

.carousel-dots {
  position: absolute;
  bottom: 12px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
}

.carousel-dots button {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  padding: 0;
}

.carousel-dots button.active {
  background: #111827;
}

.notice-grid {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px 40px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.notice {
  display: flex;
  gap: 16px;
  padding: 20px;
  border-radius: 12px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
}

.notice.important {
  background: #fef2f2;
  border-color: #fecaca;
}

.notice-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  flex-shrink: 0;
  background: #e5e7eb;
}

.notice.important .notice-icon {
  background: #ef4444;
  color: #ffffff;
}

.notice h2 {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 4px;
}

.notice p {
  font-size: 0.9rem;
  color: #4b5563;
  line-height: 1.4;
}

.catalog-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px 80px;
}

.section-heading {
  margin-bottom: 32px;
  text-align: center;
}

.section-heading h2 {
  font-size: 2rem;
  margin-bottom: 8px;
}

.section-heading p {
  color: #6b7280;
}

/* Filtros com fundo original e sem hover */
.mobile-filter-toggle {
  display: none;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  margin-bottom: 30px;
}

.filter-button {
  border: 2px solid #c7cdd4;
  background: #ffffff;
  color: #1f2937;
  border-radius: 10px;
  padding: 11px 17px;
  font: inherit;
  font-weight: 700;
  line-height: 1.2;
  cursor: pointer;
}

.filter-button.active {
  border-color: #111827;
  background: #111827;
  color: #ffffff;
  box-shadow: 0 3px 10px rgba(17, 24, 39, 0.18);
}

.clear-filter-button {
  border: 2px solid #9ca3af;
  background: #f9fafb;
  color: #374151;
  border-radius: 10px;
  padding: 11px 15px;
  font: inherit;
  font-weight: 700;
  cursor: pointer;
}

.mobile-filter-label {
  display: inline-flex;
  align-items: center;
  gap: 9px;
}

.mobile-filter-icon {
  font-size: 15px;
  line-height: 1;
}

.mobile-filter-status {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  font-weight: 700;
  color: #4b5563;
}

.mobile-filter-chevron {
  display: inline-block;
  font-size: 18px;
  line-height: 1;
  transition: transform 0.2s ease;
}

.mobile-filter-chevron.rotated {
  transform: rotate(180deg);
}

.catalog-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
}

.product-card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  background: #ffffff;
}

.product-media {
  position: relative;
  background: #f9fafb;
}

/* Tag da categoria com fundo branco */
.tag {
  position: absolute;
  top: 10px;
  left: 10px;
  background: #ffffff;
  color: #111827;
  border: 1px solid #e5e7eb;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 6px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  z-index: 2;
}

.product-media img {
  width: 100%;
  height: 220px;
  object-fit: cover;
  display: block;
  cursor: pointer;
}

.product-content {
  padding: 16px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.product-content h3 {
  font-size: 1.1rem;
  margin-bottom: 6px;
}

.product-content p {
  font-size: 0.85rem;
  color: #6b7280;
  line-height: 1.4;
  margin-bottom: 12px;
  flex-grow: 1;
}

.price-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.price {
  font-weight: 800;
  font-size: 1.1rem;
  color: #111827;
}

.badge {
  font-size: 0.75rem;
  font-weight: 700;
  background: #dcfce7;
  color: #166534;
  padding: 3px 8px;
  border-radius: 4px;
}

.product-actions {
  display: flex;
  gap: 8px;
}

.icon-button {
  width: 42px;
  height: 42px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  background: #ffffff;
  cursor: pointer;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.choose-button {
  flex-grow: 1;
  height: 42px;
  background: #111827;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
}

.order-panel {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  z-index: 200;
  display: flex;
  justify-content: flex-end;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.25s ease;
}

.order-panel.open {
  opacity: 1;
  pointer-events: auto;
}

.order-card {
  width: 100%;
  max-width: 480px;
  height: 100%;
  background: #ffffff;
  overflow-y: auto;
  padding: 24px;
  position: relative;
}

.close-button {
  position: absolute;
  top: 16px;
  right: 16px;
  font-size: 28px;
  border: none;
  background: none;
  cursor: pointer;
  line-height: 1;
}

.selected-product {
  display: flex;
  gap: 16px;
  align-items: center;
  padding-bottom: 20px;
  border-bottom: 1px solid #e5e7eb;
  margin-bottom: 20px;
}

.selected-product img {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
}

.selected-category-text {
  font-size: 0.85rem;
  color: #6b7280;
  margin-top: 2px;
}

fieldset {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 20px;
}

legend {
  font-weight: 700;
  padding: 0 6px;
  font-size: 0.9rem;
}

.check-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  cursor: pointer;
  font-size: 0.9rem;
}

.form-note {
  font-size: 0.8rem;
  color: #6b7280;
  margin-top: 8px;
}

.prescription-grid {
  display: grid;
  grid-template-columns: 40px repeat(3, 1fr);
  gap: 8px;
  align-items: center;
}

.grid-head {
  font-size: 0.75rem;
  font-weight: 700;
  text-align: center;
  color: #6b7280;
}

.eye-label {
  font-weight: 800;
  font-size: 0.9rem;
}

.prescription-grid select {
  padding: 6px;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  font-size: 0.85rem;
}

.text-label {
  display: block;
  font-weight: 700;
  margin-bottom: 6px;
  font-size: 0.9rem;
}

textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  margin-bottom: 20px;
  font-family: inherit;
  resize: vertical;
}

.primary-button.full {
  width: 100%;
}

#lightbox {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 300;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s ease;
}

#lightbox.open {
  opacity: 1;
  pointer-events: auto;
}

#lightbox img {
  max-width: 90%;
  max-height: 85vh;
  border-radius: 8px;
}

footer {
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
  padding: 40px 20px;
  text-align: center;
}

footer strong {
  font-size: 1.2rem;
}

footer p {
  color: #6b7280;
  margin: 6px 0 16px;
  font-size: 0.9rem;
}

.footer-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-bottom: 20px;
}

.footer-actions a {
  text-decoration: none;
  color: #111827;
  font-weight: 700;
  font-size: 0.9rem;
}

footer small {
  color: #9ca3af;
  font-size: 0.8rem;
}

.empty-state {
  text-align: center;
  color: #6b7280;
  padding: 40px 0;
  font-size: 1.1rem;
}

/* Botão Menu Hambúrguer (Oculto no Desktop) */
.mobile-menu-toggle {
  display: none;
  flex-direction: column;
  justify-content: space-around;
  width: 32px;
  height: 28px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 101;
  -webkit-tap-highlight-color: transparent;
}

.mobile-menu-toggle .bar {
  width: 100%;
  height: 3px;
  background-color: #111827;
  border-radius: 4px;
  transition: transform 0.3s ease, opacity 0.3s ease;
}

/* Animação do 'X' ao abrir */
.mobile-menu-toggle .bar-top {
  transform: translateY(9px) rotate(45deg);
}

.mobile-menu-toggle .bar-mid {
  opacity: 0;
}

.mobile-menu-toggle .bar-bot {
  transform: translateY(-9px) rotate(-45deg);
}

@media (max-width: 768px) {
  .hero {
    grid-template-columns: 1fr;
  }

  .notice-grid {
    grid-template-columns: 1fr;
  }

  .mobile-menu-toggle {
    display: flex;
  }

  .nav-links {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    background: #ffffff;
    flex-direction: column;
    padding: 20px;
    gap: 16px;
    border-bottom: 1px solid #e5e7eb;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    z-index: 100;
  }

  .nav-links.nav-open {
    display: flex;
  }

  .nav-links a {
    width: 100%;
    text-align: center;
    padding: 10px 0;
  }

  .mobile-filter-toggle {
    width: 100%;
    min-height: 50px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin: 0 0 10px;
    padding: 13px 15px;
    border: 2px solid #c7cdd4;
    border-radius: 11px;
    background: #ffffff;
    color: #111827;
    font: inherit;
    font-weight: 800;
    text-align: left;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(17, 24, 39, 0.06);
  }

  .mobile-filter-toggle:active {
    transform: scale(0.99);
  }

  .filters {
    display: none;
    width: 100%;
    padding: 12px;
    margin-bottom: 18px;
    border: 1px solid #d1d5db;
    border-radius: 12px;
    background: #f8fafc;
    box-shadow: 0 5px 18px rgba(17, 24, 39, 0.08);
  }

  .filters.mobile-open {
    display: flex;
  }

  .filter-button {
    flex: 1 1 calc(50% - 10px);
    min-height: 45px;
    padding: 10px 12px;
  }

  .clear-filter-button {
    width: 100%;
    min-height: 44px;
    margin-top: 2px;
  }
}

@media (max-width: 390px) {
  .filter-button {
    flex-basis: 100%;
  }
}
</style>
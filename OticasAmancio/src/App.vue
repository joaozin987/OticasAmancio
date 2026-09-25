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

      <!-- Links de Navegação -->
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
            <span v-if="hasGallery(product)" class="photo-count">{{ product.images.length }} fotos</span>
            <img :src="product.image" :alt="product.name" loading="lazy" decoding="async" @click="openProductMedia(product)">
          </div>
          <div class="product-content">
            <h3>{{ product.name }}</h3>
            <p>{{ product.description }}</p>
            <div class="price-row">
              <span class="price">{{ product.price }}</span>
              <span class="badge">Armação disponível</span>
            </div>
            <div class="product-actions">
              <button class="icon-button" type="button" :aria-label="`Ampliar ${product.name}`" @click="openProductMedia(product)">⌕</button>
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
        <img :src="selectedProduct.image" :alt="selectedProduct.name" decoding="async">
        <div>
          <p class="eyebrow">Armação escolhida</p>
          <h2 id="orderTitle">{{ selectedProduct.name }}</h2>
          <p>{{ categories[selectedProduct.category] }}</p>
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

  <!-- Galeria para modelos com mais de uma foto (ex.: clipom e solares) -->
  <div
    v-if="galleryProduct"
    class="gallery-modal"
    role="dialog"
    aria-modal="true"
    :aria-label="`Fotos de ${galleryProduct.name}`"
    @click.self="closeGallery"
  >
    <div class="gallery-card">
      <button class="gallery-close" type="button" aria-label="Fechar galeria" @click="closeGallery">×</button>

      <div class="gallery-stage">
        <button class="gallery-arrow prev" type="button" aria-label="Foto anterior" @click="previousGalleryImage">‹</button>
        <img
          :key="galleryProduct.images[galleryImageIndex]"
          :src="galleryProduct.images[galleryImageIndex]"
          :alt="`${galleryProduct.name} - foto ${galleryImageIndex + 1}`"
        >
        <button class="gallery-arrow next" type="button" aria-label="Próxima foto" @click="nextGalleryImage">›</button>
      </div>

      <div class="gallery-thumbs">
        <button
          v-for="(image, index) in galleryProduct.images"
          :key="image"
          type="button"
          :class="{ active: galleryImageIndex === index }"
          :aria-label="`Ver foto ${index + 1}`"
          @click="selectGalleryImage(index)"
        >
          <img :src="image" alt="" loading="lazy" decoding="async">
        </button>
      </div>

      <div class="gallery-footer">
        <div>
          <strong>{{ galleryProduct.name }}</strong>
          <span>{{ galleryImageIndex + 1 }} de {{ galleryProduct.images.length }}</span>
        </div>
        <button class="choose-button" type="button" @click="chooseFromGallery">Escolher armação</button>
      </div>
    </div>
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
const galleryProduct = ref(null);
const galleryImageIndex = ref(0);
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

const hasGallery = (product) => Array.isArray(product.images) && product.images.length > 1;

const openGallery = (product) => {
  galleryProduct.value = product;
  galleryImageIndex.value = 0;
};

const closeGallery = () => {
  galleryProduct.value = null;
  galleryImageIndex.value = 0;
};

// Abre a galeria se o modelo tiver várias fotos; se tiver só uma, abre a imagem ampliada
const openProductMedia = (product) => {
  if (hasGallery(product)) {
    openGallery(product);
  } else {
    openImage(product.image);
  }
};

const nextGalleryImage = () => {
  if (!galleryProduct.value?.images?.length) return;

  galleryImageIndex.value =
    (galleryImageIndex.value + 1) %
    galleryProduct.value.images.length;
};

const previousGalleryImage = () => {
  if (!galleryProduct.value?.images?.length) return;

  galleryImageIndex.value =
    (galleryImageIndex.value - 1 + galleryProduct.value.images.length) %
    galleryProduct.value.images.length;
};

const selectGalleryImage = (index) => {
  galleryImageIndex.value = index;
};

const categories = {
  polarizadas: "Polarizadas",
  "masculina-metal": "Masculina metal",
  "masculina-acetato": "Masculina acetato",
  "masculina-classica": "Masculina clássica",
  "masculina-oakley": "Masculina esportiva",
  "feminina-acetato": "Feminina acetato",
  "feminina-metal": "Feminina metal",
  "feminina-clipom-solar": "Feminina clipom e solar",
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
    description: "Armação unissex versátil, confortável para o dia a dia."
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
  },
  {
    id: "oa-f079",
    name: "Acetato 01",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-01.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f080",
    name: "Acetato 02",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-02.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f081",
    name: "Acetato 03",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-03.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f082",
    name: "Acetato 04",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-04.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f083",
    name: "Acetato 05",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-05.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f084",
    name: "Acetato 06",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-06.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f085",
    name: "Acetato 07",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-07.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f086",
    name: "Acetato 08",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-08.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f087",
    name: "Acetato 09",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-09.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f088",
    name: "Acetato 10",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-10.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f089",
    name: "Acetato 11",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-11.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f090",
    name: "Acetato 12",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-12.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f091",
    name: "Acetato 13",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-13.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f092",
    name: "Acetato 14",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-14.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f093",
    name: "Acetato 15",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-15.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f094",
    name: "Acetato 16",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-16.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f095",
    name: "Acetato 17",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-17.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f096",
    name: "Acetato 18",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-18.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f097",
    name: "Acetato 19",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-19.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f098",
    name: "Acetato 20",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-20.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f099",
    name: "Acetato 21",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-21.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f100",
    name: "Acetato 22",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-22.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f101",
    name: "Acetato 23",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-23.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f102",
    name: "Acetato 24",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-24.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f103",
    name: "Acetato 25",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-25.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f104",
    name: "Acetato 26",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-26.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f105",
    name: "Acetato 27",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-27.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f106",
    name: "Acetato 28",
    category: "feminina-acetato",
    image: imagePath("fem-acetato-28.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em acetato, leve, resistente e confortável para uso diário."
  },
  {
    id: "oa-f107",
    name: "Metal 01",
    category: "feminina-metal",
    image: imagePath("fem-metal-01.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f108",
    name: "Metal 02",
    category: "feminina-metal",
    image: imagePath("fem-metal-02.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f109",
    name: "Metal 03",
    category: "feminina-metal",
    image: imagePath("fem-metal-03.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f110",
    name: "Metal 04",
    category: "feminina-metal",
    image: imagePath("fem-metal-04.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f111",
    name: "Metal 05",
    category: "feminina-metal",
    image: imagePath("fem-metal-05.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f112",
    name: "Metal 06",
    category: "feminina-metal",
    image: imagePath("fem-metal-06.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f113",
    name: "Metal 07",
    category: "feminina-metal",
    image: imagePath("fem-metal-07.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f114",
    name: "Metal 08",
    category: "feminina-metal",
    image: imagePath("fem-metal-08.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f115",
    name: "Metal 09",
    category: "feminina-metal",
    image: imagePath("fem-metal-09.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f116",
    name: "Metal 10",
    category: "feminina-metal",
    image: imagePath("fem-metal-10.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f117",
    name: "Metal 11",
    category: "feminina-metal",
    image: imagePath("fem-metal-11.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f118",
    name: "Metal 12",
    category: "feminina-metal",
    image: imagePath("fem-metal-12.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f119",
    name: "Metal 13",
    category: "feminina-metal",
    image: imagePath("fem-metal-13.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f120",
    name: "Metal 14",
    category: "feminina-metal",
    image: imagePath("fem-metal-14.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f121",
    name: "Metal 15",
    category: "feminina-metal",
    image: imagePath("fem-metal-15.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f122",
    name: "Metal 16",
    category: "feminina-metal",
    image: imagePath("fem-metal-16.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f123",
    name: "Metal 17",
    category: "feminina-metal",
    image: imagePath("fem-metal-17.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f124",
    name: "Metal 18",
    category: "feminina-metal",
    image: imagePath("fem-metal-18.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f125",
    name: "Metal 19",
    category: "feminina-metal",
    image: imagePath("fem-metal-19.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f126",
    name: "Metal 20",
    category: "feminina-metal",
    image: imagePath("fem-metal-20.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f127",
    name: "Metal 21",
    category: "feminina-metal",
    image: imagePath("fem-metal-21.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f128",
    name: "Metal 22",
    category: "feminina-metal",
    image: imagePath("fem-metal-22.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f129",
    name: "Metal 23",
    category: "feminina-metal",
    image: imagePath("fem-metal-23.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f130",
    name: "Metal 24",
    category: "feminina-metal",
    image: imagePath("fem-metal-24.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f131",
    name: "Metal 25",
    category: "feminina-metal",
    image: imagePath("fem-metal-25.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f132",
    name: "Metal 26",
    category: "feminina-metal",
    image: imagePath("fem-metal-26.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f133",
    name: "Metal 27",
    category: "feminina-metal",
    image: imagePath("fem-metal-27.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f134",
    name: "Metal 28",
    category: "feminina-metal",
    image: imagePath("fem-metal-28.jpg"),
    price: "R$ 120,00",
    description: "Armação feminina em metal, leve, delicada e com acabamento resistente."
  },
  {
    id: "oa-f135",
    name: "Clipom 01",
    category: "feminina-clipom-solar",
    image: imagePath("fem-clipom-01-1.jpg"),
    images: [
      imagePath("fem-clipom-01-1.jpg"),
      imagePath("fem-clipom-01-2.jpg"),
      imagePath("fem-clipom-01-3.jpg"),
      imagePath("fem-clipom-01-4.jpg")
    ],
    price: "R$ 120,00",
    description: "Armação feminina em acetato com clipom solar encaixável: óculos de grau e de sol em uma peça só."
  },
  {
    id: "oa-f136",
    name: "Clipom 02",
    category: "feminina-clipom-solar",
    image: imagePath("fem-clipom-02-1.jpg"),
    images: [
      imagePath("fem-clipom-02-1.jpg"),
      imagePath("fem-clipom-02-2.jpg")
    ],
    price: "R$ 120,00",
    description: "Armação feminina em acetato com clipom solar encaixável: óculos de grau e de sol em uma peça só."
  },
  {
    id: "oa-f137",
    name: "MilMil Solar 01",
    category: "feminina-clipom-solar",
    image: imagePath("fem-solar-milmil-01-1.jpg"),
    images: [
      imagePath("fem-solar-milmil-01-1.jpg"),
      imagePath("fem-solar-milmil-01-2.jpg"),
      imagePath("fem-solar-milmil-01-3.jpg")
    ],
    price: "R$ 120,00",
    description: "Óculos solar feminino em acetato, formato retangular com detalhe dourado na haste."
  },
  {
    id: "oa-f138",
    name: "MilMil Solar 02",
    category: "feminina-clipom-solar",
    image: imagePath("fem-solar-milmil-02.jpg"),
    price: "R$ 120,00",
    description: "Óculos solar feminino em acetato, formato arredondado e acabamento elegante."
  },
  {
    id: "oa-f139",
    name: "MilMil Metal Modelo 21",
    category: "feminina-clipom-solar",
    image: imagePath("fem-metal-milmil-21-1.jpg"),
    images: [
      imagePath("fem-metal-milmil-21-1.jpg"),
      imagePath("fem-metal-milmil-21-2.jpg")
    ],
    price: "R$ 120,00",
    description: "Óculos solar feminino em metal com lente degradê e visual sofisticado."
  },
  {
    id: "oa-f140",
    name: "MilMil Metal Hexagonal",
    category: "feminina-clipom-solar",
    image: imagePath("fem-metal-milmil-hexagonal-1.jpg"),
    images: [
      imagePath("fem-metal-milmil-hexagonal-1.jpg"),
      imagePath("fem-metal-milmil-hexagonal-2.jpg")
    ],
    price: "R$ 120,00",
    description: "Óculos solar feminino hexagonal, com hastes em acetato e detalhe dourado."
  },
  {
    id: "oa-f141",
    name: "MilMil Metal Oval 01",
    category: "feminina-clipom-solar",
    image: imagePath("fem-metal-milmil-oval-01.jpg"),
    price: "R$ 120,00",
    description: "Óculos solar feminino em metal, formato oval, leve e moderno."
  },
  {
    id: "oa-f142",
    name: "MilMil Metal Oval 02",
    category: "feminina-clipom-solar",
    image: imagePath("fem-metal-milmil-oval-02.jpg"),
    price: "R$ 120,00",
    description: "Óculos solar feminino em metal, formato oval com hastes trabalhadas."
  }
];

const featuredImages = [
  {
    src: imagePath("masc-oakley-vilao-vilao-1.jpg"),
    alt: "Armação Oakley Vilão em destaque"
  },
  {
    src: imagePath("fem-clipom-01-1.jpg"),
    alt: "Armação feminina com clipom em destaque"
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

const chooseFromGallery = () => {
  const product = galleryProduct.value;
  closeGallery();
  if (product) openOrderPanel(product);
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

const handleKeydown = (event) => {
  if (event.key === "Escape") {
    closeGallery();
    closeOrderPanel();
    closeImage();
    return;
  }

  if (galleryProduct.value) {
    if (event.key === "ArrowRight") nextGalleryImage();
    if (event.key === "ArrowLeft") previousGalleryImage();
  }
};

onMounted(() => {
  startCarousel();
  document.addEventListener("keydown", handleKeydown);
});

onBeforeUnmount(() => {
  stopCarousel();
  document.removeEventListener("keydown", handleKeydown);
});
</script>

<style scoped>
/* Ajustes dos filtros do catálogo */
.mobile-filter-toggle {
  display: none;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
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

/* Botão Menu Hambúrguer Base */
.mobile-menu-toggle {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 28px;
  height: 20px;
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

.mobile-menu-toggle .bar-top {
  transform: translateY(8px) rotate(45deg);
}

.mobile-menu-toggle .bar-mid {
  opacity: 0;
}

.mobile-menu-toggle .bar-bot {
  transform: translateY(-8px) rotate(-45deg);
}

/* ==========================================================
   Selo "X fotos" no card + Galeria de fotos do modelo
   ========================================================== */
.product-media {
  position: relative;
}

.photo-count {
  position: absolute;
  right: 10px;
  bottom: 10px;
  z-index: 2;
  padding: 5px 10px;
  border-radius: 999px;
  background: rgba(17, 24, 39, 0.78);
  color: #ffffff;
  font-size: 0.78rem;
  font-weight: 700;
  pointer-events: none;
}

.gallery-modal {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  background: rgba(10, 12, 16, 0.82);
}

.gallery-card {
  position: relative;
  width: min(760px, 100%);
  max-height: calc(100vh - 32px);
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  border-radius: 16px;
  background: #ffffff;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.35);
  overflow: auto;
}

.gallery-close {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 3;
  width: 38px;
  height: 38px;
  border: none;
  border-radius: 50%;
  background: rgba(17, 24, 39, 0.75);
  color: #ffffff;
  font-size: 24px;
  line-height: 1;
  cursor: pointer;
}

.gallery-stage {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: #f3f4f6;
  overflow: hidden;
}

.gallery-stage img {
  display: block;
  width: 100%;
  max-height: 62vh;
  object-fit: contain;
}

.gallery-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 2;
  width: 42px;
  height: 42px;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  color: #111827;
  font-size: 28px;
  line-height: 1;
  cursor: pointer;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
}

.gallery-arrow.prev {
  left: 10px;
}

.gallery-arrow.next {
  right: 10px;
}

.gallery-thumbs {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 2px;
}

.gallery-thumbs button {
  flex: 0 0 auto;
  width: 64px;
  height: 64px;
  padding: 0;
  border: 2px solid transparent;
  border-radius: 10px;
  background: #f3f4f6;
  overflow: hidden;
  cursor: pointer;
  opacity: 0.65;
}

.gallery-thumbs button.active {
  border-color: #5b6f48;
  opacity: 1;
}

.gallery-thumbs img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.gallery-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.gallery-footer strong {
  display: block;
  color: #111827;
}

.gallery-footer span {
  font-size: 0.85rem;
  color: #6b7280;
}

/* ==========================================================
   Ajustes Mobile: 768px até telas ultra-compactas (<= 400px)
   ========================================================== */
/* ==========================================================
   Header Mobile Verde Oficial (igual ao Desktop):
   - Fundo verde oliva (#5b6f48)
   - Logo maior na ponta esquerda
   - Toggle hambúrguer/X branco na ponta direita
   - Menu abre empurrando a seção hero com divisória
   ========================================================== */
@media (max-width: 768px) {
  .site-header {
    width: 100% !important;
    position: relative !important;
    background-color: #5b6f48 !important; /* Cor verde oficial do seu desktop */
    border-bottom: 1px solid rgba(255, 255, 255, 0.15) !important;
  }

  .nav {
    display: flex !important;
    flex-wrap: wrap !important;
    flex-direction: row !important;
    align-items: center !important;
    justify-content: space-between !important;
    width: 100% !important;
    padding: 14px 18px !important;
    box-sizing: border-box !important;
    background-color: #5b6f48 !important;
  }

  /* Logo maior e cravada na esquerda */
  .header-logo {
    display: flex !important;
    align-items: center !important;
    margin: 0 !important;
    flex: 0 0 auto !important;
  }

  .header-logo img {
    height: 54px !important; /* Logo grande e nítida */
    width: auto !important;
    max-width: 190px !important;
    display: block !important;
    object-fit: contain;
  }

  /* Botão Hambúrguer / X branco na ponta direita */
  .mobile-menu-toggle {
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    width: 28px !important;
    height: 20px !important;
    padding: 0 !important;
    margin: 0 !important;
    background: transparent !important;
    border: none !important;
    cursor: pointer !important;
    flex-shrink: 0 !important;
    z-index: 102;
  }

  /* Cor branca nas barras para contrastar com o verde */
  .mobile-menu-toggle .bar {
    width: 100%;
    height: 3px;
    background-color: #ffffff !important;
    border-radius: 4px;
  }

  /* Gaveta do menu aberta */
  .nav-links {
    display: none;
    width: 100% !important;
    position: static !important;
    box-sizing: border-box !important;
    flex-direction: column !important;
    padding: 18px 0 10px 0 !important;
    gap: 12px !important;
    background-color: #5b6f48 !important;
    border-top: 1px solid rgba(255, 255, 255, 0.12) !important;
  }

  .nav-links.nav-open {
    display: flex !important;
  }

  /* Estilização dos botões no estilo do tema */
  .nav-links a {
    width: 100% !important;
    box-sizing: border-box !important;
    text-align: center !important;
    padding: 12px 16px !important;
    border-radius: 25px !important; /* Arredondado igual aos botões do desktop */
    font-weight: 700 !important;
    text-decoration: none !important;
    display: block !important;
    font-size: 0.95rem !important;
    transition: all 0.2s ease;
  }

  .nav-links a.cata {
    background: rgba(255, 255, 255, 0.15) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.4) !important;
  }

  .nav-links a.whatsapp-link {
    background: #ffffff !important;
    color: #5b6f48 !important;
    border: 1px solid #ffffff !important;
  }

  /* Galeria no celular */
  .gallery-modal {
    padding: 10px;
  }

  .gallery-card {
    padding: 12px;
  }

  .gallery-stage img {
    max-height: 55vh;
  }

  .gallery-arrow {
    width: 36px;
    height: 36px;
    font-size: 24px;
  }

  .gallery-footer .choose-button {
    width: 100%;
  }
}

/* Telas menores (iPhone SE / 400px e abaixo) */
@media (max-width: 400px) {
  .nav {
    padding: 12px 14px !important;
  }

  .header-logo img {
    height: 48px !important;
  }

  .mobile-menu-toggle {
    width: 26px !important;
    height: 18px !important;
  }

  .gallery-thumbs button {
    width: 54px;
    height: 54px;
  }
}
</style>
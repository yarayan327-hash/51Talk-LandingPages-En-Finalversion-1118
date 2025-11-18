/**
 * Final Multilingual Support for 51Talk Landing Page
 * Supports Chinese (zh), English (en), Arabic (ar)
 * Default language: Chinese
 */

class FinalI18n {
    constructor() {
        this.currentLanguage = 'zh'; // Default to Chinese
        this.translations = {};
        this.contentMapping = {};
        this.init();
    }

    async init() {
        console.log('🚀 Initializing i18n system...');

        // ✅ Step 1: Load content mapping FIRST (highest priority)
        console.log('📋 Step 1: Loading content mapping...');
        await this.loadContentMapping();
        console.log('✅ Content mapping loaded');

        // ✅ Step 2: Load language JSON SECOND
        console.log('🌐 Step 2: Loading language JSON...');
        await this.loadLanguage(this.currentLanguage);
        console.log('✅ Language loaded');

        // ✅ Step 3: Setup UI after content is ready
        console.log('🔧 Step 3: Setup UI...');
        this.setupDirectionHandling();
        this.addLanguageSelector();

        // ✅ Step 4: Final verification
        this.verifyLoadingComplete();
        console.log('✅ i18n system initialization completed');
    }

    // Verify all loading completed successfully
    verifyLoadingComplete() {
        const totalElements = document.querySelectorAll('[data-i18n]').length;
        const translatedElements = document.querySelectorAll('[data-i18n]').filter(el => el.textContent.trim() !== '').length;

        console.log(`📊 Translation Status: ${translatedElements}/${totalElements} elements translated`);

        if (translatedElements < totalElements) {
            console.warn(`⚠️  Warning: ${totalElements - translatedElements} translation keys missing`);
        }
    }

    // Load content mapping JSON
    async loadContentMapping() {
        try {
            // Get current page name from URL
            const pageName = window.location.pathname.split('/').pop().replace('.html', '');
            const validPages = ['GradeUp', 'ScoreBoost', 'SpeakUp'];

            if (!pageName || validPages.includes(pageName)) {
                const mappingPage = pageName || 'GradeUp';
                const response = await fetch(`./assets/content/content-mapping-${mappingPage}.json`);
                if (response.ok) {
                    const data = await response.json();
                    // Handle both mapping formats
                    if (data.mappings) {
                        this.contentMapping = data;
                    } else {
                        this.contentMapping = { mappings: {} };
                        // Convert array format to object format
                        if (Array.isArray(data)) {
                            data.forEach(item => {
                                if (item.fieldKey) {
                                    this.contentMapping.mappings[item.fieldKey] = {
                                        zh: item.zh,
                                        en: item.en,
                                        ar: item.ar
                                    };
                                }
                            });
                        }
                    }
                    console.log('Content mapping loaded successfully');
                }
            }
        } catch (error) {
            console.error('Failed to load content mapping:', error);
        }
    }

    // Load translation file
    async loadLanguage(lang) {
        try {
            const response = await fetch(`./assets/locales/${lang}.json`);
            if (!response.ok) {
                throw new Error(`Failed to load language ${lang}: HTTP ${response.status}`);
            }
            this.translations = await response.json();
            this.currentLanguage = lang;
            this.updatePageLanguage();
            this.updateHTMLLang();
            this.updateDirection();
        } catch (error) {
            console.error(`❌ FAILED TO LOAD LANGUAGE: ${lang}`, error);

            // ❌ STRICT FAILURE: Do NOT fallback to innerHTML, keep current language
            // Do NOT automatically switch to Chinese - this prevents fallback to placeholder text
            alert(`Language loading failed: ${lang}`);

            // Still attempt to load Chinese as absolute last resort
            if (lang !== 'zh') {
                console.log(`Attempting fallback to Chinese (zh)...`);
                await this.loadLanguage('zh');
            } else {
                // Even Chinese failed - clear page to avoid displaying placeholder text
                console.error('Critical: Chinese language also failed to load!');
            }
        }
    }

    // Update all text elements with data-i18n attribute
    updatePageLanguage() {
        const elements = document.querySelectorAll('[data-i18n]');
        elements.forEach(element => {
            const key = element.dataset.i18n;
            const translation = this.getTranslationFromMapping(key) || this.getNestedTranslation(key);
            // ✅ FIXED: Always replace content, even if no translation found (use empty string)
            element.textContent = translation || '';
        });
    }

    // Get translation from content mapping
    getTranslationFromMapping(key) {
        if (this.contentMapping.mappings && this.contentMapping.mappings[key]) {
            const mapping = this.contentMapping.mappings[key];
            return mapping.content ? mapping.content[this.currentLanguage] : mapping[this.currentLanguage];
        }
        return null;
    }

    // Get nested translation using dot notation
    getNestedTranslation(key) {
        return key.split('.').reduce((obj, k) => obj && obj[k], this.translations);
    }

    // Update HTML lang attribute
    updateHTMLLang() {
        document.documentElement.lang = this.currentLanguage;
    }

    // Update text direction
    updateDirection() {
        const isRTL = this.currentLanguage === 'ar';
        document.documentElement.dir = isRTL ? 'rtl' : 'ltr';

        // Add/remove RTL class for additional styling if needed
        if (isRTL) {
            document.body.classList.add('rtl');
        } else {
            document.body.classList.remove('rtl');
        }
    }

    // Handle direction-specific styling
    setupDirectionHandling() {
        // Add CSS for RTL-specific adjustments
        const style = document.createElement('style');
        style.textContent = `
            .rtl .grid {
                direction: rtl;
            }
            .rtl .flex {
                direction: rtl;
            }
            .rtl .text-center {
                text-align: center !important;
            }
            .rtl .text-left {
                text-align: right !important;
            }
            .rtl .text-right {
                text-align: left !important;
            }
            .rtl .ml-8 {
                margin-left: 0;
                margin-right: 2rem;
            }
            .rtl .mr-8 {
                margin-right: 0;
                margin-left: 2rem;
            }
            .rtl .pl-8 {
                padding-left: 0;
                padding-right: 2rem;
            }
            .rtl .pr-8 {
                padding-right: 0;
                padding-left: 2rem;
            }
            .rtl .order-1 {
                order: 2;
            }
            .rtl .order-2 {
                order: 1;
            }
            /* For language selector positioning in RTL */
            .rtl .language-selector {
                left: 20px;
                right: auto;
            }

            /* Ensure language selector is always visible */
            .language-selector {
                z-index: 9999 !important;
            }
        `;
        document.head.appendChild(style);
    }

    // Add language selector to page
    addLanguageSelector() {
        const selectorHTML = `
            <div class="language-selector fixed top-6 right-6 z-50 bg-white rounded-lg shadow-xl p-3 border border-gray-300" style="min-width: 120px;">
                <label for="language-selector" class="block text-xs font-semibold text-gray-600 mb-1">Language / 语言</label>
                <select id="language-selector" class="w-full bg-transparent text-sm font-medium text-text-primary focus:outline-none cursor-pointer border border-gray-200 rounded px-2 py-1">
                    <option value="zh">中文</option>
                    <option value="en">English</option>
                    <option value="ar">العربية</option>
                </select>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', selectorHTML);

        // Setup selector event listeners
        const selector = document.getElementById('language-selector');
        if (selector) {
            selector.value = this.currentLanguage;
            selector.addEventListener('change', (e) => {
                this.switchLanguage(e.target.value);
            });
        }
    }

    // Switch language - with proper error handling and no fallback
    async switchLanguage(lang) {
        if (lang !== this.currentLanguage) {
            try {
                console.log(`🔄 Switching to language: ${lang}`);
                await this.loadLanguage(lang);

                // Only update preferences if successfully loaded
                localStorage.setItem('preferred-language', lang);

                // Update selector if it exists
                const selector = document.getElementById('language-selector');
                if (selector) {
                    selector.value = lang;
                }

                console.log(`✅ Language switch to ${lang} completed successfully`);
            } catch (error) {
                console.error(`❌ Language switch to ${lang} failed:`, error);
                alert(`Language switch failed: ${lang}. Please try again.`);
            }
        }
    }

    // Get current language
    getCurrentLanguage() {
        return this.currentLanguage;
    }

    // Get translation for a specific key
    t(key) {
        // ❌ REMOVED: Prevent fallback to key itself
        const translation = this.getTranslationFromMapping(key) || this.getNestedTranslation(key);
        return translation || '';
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.i18n = new FinalI18n();

    // Load saved language preference if exists
    const savedLanguage = localStorage.getItem('preferred-language');
    if (savedLanguage && ['ar', 'zh', 'en'].includes(savedLanguage)) {
        window.i18n.switchLanguage(savedLanguage);
    }
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FinalI18n;
}
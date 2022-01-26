class DesktopSubMenu {
    static selector() {
        return '[data-desktop-menu] [data-open-subnav]';
    }

    static parentSelector() {
        return this.node.closest('[data-has-subnav]');
    }

    constructor(node) {
        this.node = node;
        this.toggleNode = this.node.closest('[data-has-subnav]');
        this.allToggleNodes = document.querySelectorAll(
            '[data-desktop-menu] [data-has-subnav]',
        );
        this.activeClass = 'active';
        this.bindEventListeners();
    }

    bindEventListeners() {
        this.node.addEventListener('click', (e) => {
            e.preventDefault();

            // Close other menu items that may be open
            this.allToggleNodes.forEach((item) => {
                if (item !== this.toggleNode) {
                    item.classList.remove(this.activeClass);
                    item.querySelector('[data-open-subnav]').setAttribute(
                        'aria-expanded',
                        'false',
                    );
                }
            });

            if (this.toggleNode.classList.contains('active')) {
                this.toggleNode.classList.remove('active');
                this.node.setAttribute('aria-expanded', 'false');
            } else {
                this.toggleNode.classList.add('active');
                this.node.setAttribute('aria-expanded', 'true');
            }
        });
    }
}

export default DesktopSubMenu;

package androidx.media3.exoplayer.libass;

import androidx.annotation.Nullable;

/**
 * Stand-in for the libass configuration holder that FongMi/media does not publish.
 *
 * <p>Values are accepted and dropped. Nothing reaches libass, because
 * {@link LibassPlaybackSession#isAvailable()} is false and every call site checks it
 * first.
 */
@SuppressWarnings("unused")
public final class LibassConfiguration {

    private LibassConfiguration() {
    }

    /** Mirrors the fluent API used by ExoPlayerSession. */
    public static final class Builder {

        private String fontConfig;
        private String fontsDirectory;
        private String defaultFontFamily;
        private int maximumRenderPixels;
        private int maximumGlyphCount;
        private int maximumBitmapCacheSizeMb;

        public Builder setFontConfig(@Nullable String fontConfig) {
            this.fontConfig = fontConfig;
            return this;
        }

        public Builder setFontsDirectory(@Nullable String fontsDirectory) {
            this.fontsDirectory = fontsDirectory;
            return this;
        }

        public Builder setDefaultFontFamily(@Nullable String defaultFontFamily) {
            this.defaultFontFamily = defaultFontFamily;
            return this;
        }

        public Builder setMaximumRenderPixels(int maximumRenderPixels) {
            this.maximumRenderPixels = maximumRenderPixels;
            return this;
        }

        public Builder setMaximumGlyphCount(int maximumGlyphCount) {
            this.maximumGlyphCount = maximumGlyphCount;
            return this;
        }

        public Builder setMaximumBitmapCacheSizeMb(int maximumBitmapCacheSizeMb) {
            this.maximumBitmapCacheSizeMb = maximumBitmapCacheSizeMb;
            return this;
        }

        public LibassConfiguration build() {
            return new LibassConfiguration();
        }
    }
}

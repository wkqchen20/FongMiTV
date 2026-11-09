package androidx.media3.exoplayer.libass;

import androidx.annotation.Nullable;
import androidx.media3.common.MediaItem;
import androidx.media3.exoplayer.Renderer;
import androidx.media3.extractor.ExtractorsFactory;
import androidx.media3.extractor.text.SubtitleParser;

/**
 * Stand-in for the libass playback session that FongMi/media does not publish.
 *
 * <p>This class is where the substitution is anchored: {@link #isAvailable()} answers
 * false unconditionally, so the app never asks the missing renderer to do anything and
 * settles back onto the stock media3 subtitle path.
 */
@SuppressWarnings("unused")
public final class LibassPlaybackSession {

    /**
     * The pieces an libass-aware media source factory would need. Only the two public
     * fields read by ExoMediaSourceFactory are modelled.
     */
    public static final class MediaComponents {

        public final ExtractorsFactory extractorsFactory;
        public final SubtitleParser.Factory subtitleParserFactory;

        public MediaComponents(ExtractorsFactory extractorsFactory, SubtitleParser.Factory subtitleParserFactory) {
            this.extractorsFactory = extractorsFactory;
            this.subtitleParserFactory = subtitleParserFactory;
        }
    }

    private final LibassConfiguration configuration;
    private final boolean enabled;

    public LibassPlaybackSession(LibassConfiguration configuration, boolean enabled) {
        this.configuration = configuration;
        this.enabled = enabled;
    }

    /**
     * Always false. ExoMediaSourceFactory skips its libass media source and ExoUtil skips
     * its clock renderer on this answer alone.
     */
    public boolean isAvailable() {
        return false;
    }

    /** Unreachable while {@link #isAvailable()} is false. */
    public MediaComponents createMediaComponents(MediaItem mediaItem, ExtractorsFactory extractorsFactory) {
        throw new UnsupportedOperationException("libass is unavailable in this build");
    }

    /** Unreachable while {@link #isAvailable()} is false. */
    public Renderer createClockRenderer() {
        throw new UnsupportedOperationException("libass is unavailable in this build");
    }

    public void setPreloadMediaItem(@Nullable MediaItem mediaItem) {
    }

    public void setBottomPositionFraction(float fraction) {
    }

    public void setSecondaryBottomPositionFraction(float fraction) {
    }

    public void setFontScale(float scale, boolean apply) {
    }

    public void close() {
    }
}

package androidx.media3.ui.libass;

import androidx.annotation.Nullable;
import androidx.media3.exoplayer.ExoPlayer;
import androidx.media3.exoplayer.libass.LibassPlaybackSession;
import androidx.media3.exoplayer.libass.LibassSubtitleController;
import androidx.media3.ui.CaptionStyleCompat;
import androidx.media3.ui.PlayerView;
import androidx.media3.ui.SubtitleView;

/**
 * Stand-in for the libass view controller that FongMi/media does not publish.
 *
 * <p>Drops the style override and never binds a second view. Subtitle styling is
 * unaffected: PlaybackActivity and SubtitleSettingPanel apply it through
 * SubtitleSetting.applyStyle on the stock SubtitleView, independently of this class.
 */
@SuppressWarnings("unused")
public final class LibassPlayerViewController {

    /** Mirrors the callback shape the caller passes as a method reference. */
    public interface SecondarySubtitleViewConfigurator {

        void configure(SubtitleView subtitleView);
    }

    public LibassPlayerViewController(ExoPlayer player, LibassPlaybackSession session, LibassSubtitleController controller) {
    }

    public void bind(PlayerView playerView) {
    }

    public void setStyleOverride(@Nullable CaptionStyleCompat style, @Nullable String fontFamily) {
    }

    public void setSecondarySubtitleViewConfigurator(@Nullable SecondarySubtitleViewConfigurator configurator) {
    }

    public void close() {
    }
}

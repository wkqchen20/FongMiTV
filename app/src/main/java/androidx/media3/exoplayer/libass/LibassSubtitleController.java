package androidx.media3.exoplayer.libass;

import androidx.annotation.Nullable;
import androidx.media3.common.TrackSelectionOverride;
import androidx.media3.exoplayer.ExoPlayer;
import androidx.media3.exoplayer.text.SecondaryTextOutput;
import androidx.media3.exoplayer.trackselection.SecondaryTextTrackSelector;

import java.util.Collections;
import java.util.List;

/**
 * Stand-in for the libass subtitle controller that FongMi/media does not publish.
 *
 * <p>Reports an empty selection so the UI shows no second subtitle track. The boolean is
 * false rather than true to match SecondarySubtitleState.EMPTY: SubtitleSettingPanel
 * reads it as secondaryPromotedToPrimary and would otherwise force the mode label to
 * "off".
 */
@SuppressWarnings("unused")
public final class LibassSubtitleController {

    public LibassSubtitleController(ExoPlayer player, LibassPlaybackSession session, SecondaryTextTrackSelector.Factory trackSelectorFactory, SecondaryTextOutput secondaryTextOutput) {
    }

    @Nullable
    public TrackSelectionOverride getPrimaryTextTrackSelectionOverride() {
        return null;
    }

    @Nullable
    public TrackSelectionOverride getSecondaryTextTrackSelectionOverride() {
        return null;
    }

    public List<TrackSelectionOverride> getSecondaryTextTrackSelectionOverrides() {
        return Collections.emptyList();
    }

    public boolean isSecondaryTextTrackSuppressed() {
        return false;
    }

    public void setSecondaryTextTrackSelectionOverride(@Nullable TrackSelectionOverride selection) {
    }

    public void setSecondaryTextTrackAutoSelectionEnabled(boolean enabled) {
    }

    public void close() {
    }
}
